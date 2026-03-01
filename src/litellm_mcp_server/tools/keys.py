from mcp_instance import mcp
from http_client import http
from helpers import fetch_teams_lookup


@mcp.tool
def get_keys_list() -> dict:
    """Return a list of all keys in the LiteLLM server, fetching all pages."""
    all_keys = []
    page = 1
    page_size = 100

    while True:
        response = http.get("/key/list", params={"return_full_object": True, "page": page, "page_size": page_size})
        response.raise_for_status()
        data = response.json()

        all_keys.extend(data["keys"])

        if page >= data["total_pages"]:
            break
        page += 1

    teams_lookup = fetch_teams_lookup()
    for key in all_keys:
        tid = key.get("team_id")
        key["team_name"] = teams_lookup.get(tid, tid) if tid else None

    return {"keys": all_keys, "total": len(all_keys)}
