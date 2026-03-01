import asyncio
import logging
from config import SysEnv
from fastmcp.utilities.logging import get_logger
from mcp_instance import mcp

# Prometheus requirements
from prometheus_client import start_http_server
from litellm_mcp_server.metrics.metrics import MCP_SERVER_INFO, TOOL_INFO

# ------------------------------------------------------------
# Logging configuration
# ------------------------------------------------------------
logger = get_logger(__name__)

log_level = getattr(logging, SysEnv['MCP_SERVER_LOGGING_LEVEL'].upper(), logging.INFO)
logging.getLogger("fastmcp").setLevel(log_level)

# ------------------------------------------------------------
# Import all MCP Tools so their @mcp.tool decorators register
# ------------------------------------------------------------
import tools

# ------------------------------------------------------------
# Start the MCP server
# ------------------------------------------------------------
if __name__ == "__main__":
    if not SysEnv['LITELLM_API_KEY']:
        logger.error("LITELLM_API_KEY is not set. The MCP server will not be able to communicate with LiteLLM.")
        exit(1)

    logger.info("Starting MCP server with the following configuration:")
    logger.info(f"  LITELLM_BASE_URL: {SysEnv['LITELLM_BASE_URL']}")
    logger.info(f"  MCP_SERVER_LOGGING_LEVEL: {SysEnv['MCP_SERVER_LOGGING_LEVEL']}")
    logger.info(f"  MCP_SERVER_PORT: {SysEnv['MCP_SERVER_PORT']}")
    logger.debug(f"  MCP_SERVER_VERSION: {SysEnv['MCP_SERVER_VERSION']}")

    # Start Prometheus server
    start_http_server(int(SysEnv['MCP_SERVER_METRICS_PORT']), addr="0.0.0.0")
    MCP_SERVER_INFO.labels(version=SysEnv['MCP_SERVER_VERSION'], litellm_base_url=SysEnv['LITELLM_BASE_URL']).set(1)
    logger.info(f"Prometheus metrics server started on port {SysEnv['MCP_SERVER_METRICS_PORT']}")

    # Register tool info metrics from FastMCP's tool registry
    for t in asyncio.run(mcp.list_tools()):
        TOOL_INFO.labels(tool_name=t.name).set(1)
        logger.info(f"  Registered tool: {t.name}")
    
    # Start MCP server
    mcp.run(transport="http", host="0.0.0.0", port=int(SysEnv['MCP_SERVER_PORT']))
