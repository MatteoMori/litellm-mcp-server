# Users

## List Users

Returns a paginated list of all users registered on the LiteLLM proxy.

**Requires:** `proxy_admin` key.

### Endpoint

```
GET /user/list
```

### Query Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | int | 1 | Page number |
| `page_size` | int | 25 | Items per page (max 100) |
| `role` | string | — | Filter by role (`proxy_admin`, `proxy_admin_viewer`, `internal_user`, `internal_user_viewer`) |
| `user_email` | string | — | Filter by partial email match |
| `team` | string | — | Filter by team ID |
| `sort_by` | string | — | Column to sort by (`user_id`, `user_email`, `created_at`, `spend`) |
| `sort_order` | string | `asc` | Sort order (`asc` or `desc`) |

### curl

```bash
curl -X GET "http://localhost:8081/user/list?page=1&page_size=25" \
  -H "Authorization: Bearer YOUR_ADMIN_KEY"
```

### Sample Response

```json
{
  "users": [
    {
      "user_id": "a1b2c3d4-0000-0000-0000-000000000001",
      "user_email": "alice@example.com",
      "user_alias": null,
      "user_role": "internal_user",
      "spend": 0.0,
      "max_budget": null,
      "models": ["no-default-models"],
      "teams": [],
      "tpm_limit": null,
      "rpm_limit": null,
      "key_count": 0,
      "created_at": "2026-01-01T10:00:00.000000Z",
      "updated_at": "2026-01-01T10:00:00.000000Z",
      "metadata": {}
    },
    {
      "user_id": "default_user_id",
      "user_email": null,
      "user_alias": null,
      "user_role": "proxy_admin",
      "spend": 0.00002,
      "max_budget": null,
      "models": [],
      "teams": ["075130aa-0000-0000-0000-000000000001"],
      "tpm_limit": null,
      "rpm_limit": null,
      "key_count": 1,
      "created_at": "2026-01-01T09:00:00.000000Z",
      "updated_at": "2026-01-27T12:00:00.000000Z",
      "metadata": {}
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 25,
  "total_pages": 1
}
```
