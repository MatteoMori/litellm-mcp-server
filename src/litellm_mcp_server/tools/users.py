from mcp_instance import mcp
from http_client import http
from helpers import fetch_teams_lookup
from litellm_mcp_server.metrics.metrics import * # Our prometheus metrics

@mcp.tool
def get_users_list() -> dict:
    """
    Return a list of all users in the LiteLLM server
      - fetch all pages
      - lookup team names for each user and include them in the response
    """
    TOOL_CALLS.labels(tool_name='get_users_list').inc()

    all_users = []
    page = 1
    page_size = 100

    while True:
        response = http.get("/user/list", params={"page": page, "page_size": page_size})
        response.raise_for_status()
        data = response.json()

        all_users.extend(data["users"]) # concatenate users from current page to the list of all users

        if page >= data["total_pages"]:
            break
        page += 1

    teams_lookup = fetch_teams_lookup() # fetch teams information to retrieve team names for each user
    for user in all_users:
        user["team_names"] = [teams_lookup.get(tid, tid) for tid in user.get("teams", [])]

    return {"users": all_users, "total": len(all_users)}
