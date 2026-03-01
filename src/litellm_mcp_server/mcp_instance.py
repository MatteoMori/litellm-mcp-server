from config import SysEnv
from fastmcp import FastMCP

mcp = FastMCP(
    name="LiteLLM MCP Server",
    instructions="""
        This server provides insights tools to analyse data from LiteLLM Servers. You can use the following tools:
        - Call get_users_list() to get a list of users.
        - Call get_teams_list() to get a list of teams.
        - Call get_keys_list() to get a list of keys.
        - Call get_team_spend_info(team_name, start_date, end_date) to get spend information for a specific team.
    """,
    version=SysEnv['MCP_SERVER_VERSION'],
    website_url="https://github.com/MatteoMori/litellm-mcp-server",
    auth=None # TODO: Change this
)
