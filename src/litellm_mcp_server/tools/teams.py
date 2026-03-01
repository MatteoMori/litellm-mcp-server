from mcp_instance import mcp
from fastmcp.utilities.logging import get_logger
from http_client import http
from helpers import fetch_teams_lookup
from litellm_mcp_server.metrics.metrics import * # Our prometheus metrics

logger = get_logger(__name__)


@mcp.tool
def get_teams_list() -> dict:
    """Return a list of all teams in the LiteLLM server."""
    TOOL_CALLS.labels(tool_name='get_teams_list').inc()

    response = http.get("/team/list")
    response.raise_for_status()
    data = response.json()

    return {"teams": data, "total": len(data)}


@mcp.tool
def get_team_spend_info(team_name: str, start_date: str, end_date: str) -> dict:
    """
    Return aggregated spend summary for a specific team, broken down by model.
    Parameters:
    - team_name: name of the team to fetch spend info for. The tool will look up the team_id based on the team_name provided.
    - start_date: start date for the spend info ( format: YYYY-MM-DD )
    - end_date: end date for the spend info ( format: YYYY-MM-DD )
    """
    TOOL_CALLS.labels(tool_name='get_team_spend_info').inc()

    # resolve team name to team ID
    teams_lookup = fetch_teams_lookup()
    team_id = None

    logger.debug("[ Tool: get_team_spend_info ] Fetching teams info for retrieval...")
    logger.debug(teams_lookup)
    for tid, tname in teams_lookup.items():
        logger.debug("tID: %s, tName: %s", tid, tname)
        if tname == team_name:
            logger.debug("Match found for team_name '%s': team_id is %s", team_name, tid)
            team_id = tid
            break

    if not team_id:
        return {"error": f"Team '{team_name}' not found", "available_teams": list(teams_lookup.values())}

    # fetch all spend logs for this team, paginating through results
    all_logs = []
    page = 1
    page_size = 100

    while True:
        response = http.get("/spend/logs/v2", params={
            "team_id": team_id,
            "start_date": start_date,
            "end_date": end_date,
            "page": page,
            "page_size": page_size,
        })
        response.raise_for_status()
        data = response.json()

        all_logs.extend(data["data"])

        if page >= data["total_pages"]:
            break
        page += 1

    # aggregate spend by model
    by_model = {}
    total_spend = 0.0
    total_tokens = 0

    for log in all_logs:
        model = log.get("model", "unknown")
        spend = log.get("spend", 0.0)
        tokens = log.get("total_tokens", 0)

        if model not in by_model:
            by_model[model] = {"spend": 0.0, "total_tokens": 0, "requests": 0}

        by_model[model]["spend"] += spend
        by_model[model]["total_tokens"] += tokens
        by_model[model]["requests"] += 1

        total_spend += spend
        total_tokens += tokens

    return {
        "team_name": team_name,
        "team_id": team_id,
        "start_date": start_date,
        "end_date": end_date,
        "total_spend": round(total_spend, 6),
        "total_tokens": total_tokens,
        "total_requests": len(all_logs),
        "by_model": by_model,
    }
