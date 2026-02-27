# Teams

## List Teams

Returns a list of all teams on the LiteLLM proxy.

**Requires:** `proxy_admin` key.

> [!NOTE]
> The endpoint is `/team/list`, not `/team/available/` — that endpoint returns empty.

### Endpoint

```
GET /team/list
```

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `user_id` | string | No | Only return teams that this user belongs to |
| `organization_id` | string | No | Only return teams belonging to this org. Pass `default_organization` to get teams with no org. |

### curl

```bash
curl -X GET "http://localhost:8081/team/list" \
  -H "Authorization: Bearer YOUR_ADMIN_KEY"
```

### Sample Response

```json
[
  {
    "team_alias": "Admins",
    "team_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "organization_id": null,
    "members_with_roles": [
      {
        "user_id": "default_user_id",
        "user_email": null,
        "role": "admin"
      }
    ],
    "models": ["all-proxy-models"],
    "tpm_limit": null,
    "rpm_limit": null,
    "max_budget": null,
    "spend": 0.0,
    "blocked": false,
    "created_at": "2026-01-01T09:00:00.000000Z",
    "updated_at": "2026-01-01T12:00:00.000000Z"
  }
]
```

> [!NOTE]
> Unlike `/user/list`, this endpoint returns a plain array (not a paginated object).
