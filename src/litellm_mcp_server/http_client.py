import httpx
from config import SysEnv

transport = httpx.HTTPTransport(retries=3)

http = httpx.Client(
    base_url=SysEnv['LITELLM_BASE_URL'],
    headers={"Authorization": f"Bearer {SysEnv['LITELLM_API_KEY']}"},
    timeout=httpx.Timeout(30.0),
    transport=transport,
)
