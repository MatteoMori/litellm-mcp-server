import time
from http_client import http

_cache: dict[str, tuple[float, dict]] = {}
CACHE_TTL = 300  # seconds


def _cached_fetch(key: str, fetcher) -> dict:
    """Return cached result if fresh, otherwise call fetcher and cache it."""
    now = time.monotonic()
    if key in _cache:
        ts, data = _cache[key]
        if now - ts < CACHE_TTL:
            return data
    data = fetcher()
    _cache[key] = (now, data)
    return data


def fetch_teams_lookup() -> dict:
    """Returns {team_id: team_alias} for all teams, cached for CACHE_TTL seconds."""
    def _fetch():
        response = http.get("/team/list")
        response.raise_for_status()
        return {t["team_id"]: t.get("team_alias", t["team_id"]) for t in response.json()}
    return _cached_fetch("teams_lookup", _fetch)
