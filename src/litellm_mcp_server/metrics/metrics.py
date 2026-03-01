from prometheus_client import Counter, Gauge

# ------------------------------------------------------------
# Define server metrics Gauges
# ------------------------------------------------------------
MCP_SERVER_INFO = Gauge('mcp_server_info', 
                       'Information about the MCP server',
                          [
                            'version',
                            'litellm_base_url'
                          ]
                        )
TOOL_INFO = Gauge('mcp_tool_info',
                   'Information about an exposed tool',
                   [
                       'tool_name'
                   ]
                )

# ------------------------------------------------------------
# Define server metrics Counters
# ------------------------------------------------------------
TOOL_CALLS = Counter('mcp_tool_calls_total', 
                     'Total tool invocations', 
                        [
                         'tool_name'
                        ]
                    )
