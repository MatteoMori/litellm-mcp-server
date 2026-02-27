import logging
from config import SysEnv
from fastmcp.utilities.logging import get_logger
from mcp_instance import mcp

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

    mcp.run(transport="http", host="0.0.0.0", port=int(SysEnv['MCP_SERVER_PORT']))
