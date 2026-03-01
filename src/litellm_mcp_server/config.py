import os
from dotenv import load_dotenv

load_dotenv()

SysEnv = {
    'LITELLM_BASE_URL': os.getenv('LITELLM_BASE_URL', 'http://localhost:8081'),
    'LITELLM_API_KEY': os.getenv('LITELLM_API_KEY', ''),

    'MCP_SERVER_LOGGING_LEVEL': os.getenv('MCP_SERVER_LOGGING_LEVEL', 'INFO'),
    'MCP_SERVER_PORT': os.getenv('MCP_SERVER_PORT', '8000'),
    'MCP_SERVER_VERSION': os.getenv('MCP_SERVER_VERSION', 'development'),
}
