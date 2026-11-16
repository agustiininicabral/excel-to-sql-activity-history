# Data dictionary

## Actors worksheet

| Column | Destination | Rule |
|---|---|---|
| actor_user_id | BIGINT UNSIGNED | Required unique identifier |
| email | VARCHAR(254) | Trim, lowercase, validate, unique |
| display_name | VARCHAR(160) | Required, trimmed |
| is_active | BOOLEAN | Accept 0/1 or true/false |

## ActivityEvents worksheet

| Column | Destination | Rule |
|---|---|---|
| event_id | VARCHAR(40) | Required and unique |
| actor_user_id | BIGINT UNSIGNED NULL | Existing actor ID or SYSTEM |
| event_type | VARCHAR(30) | login/logout/create/update/delete/export/failed_login |
| entity_type | VARCHAR(30) | auth/user/order/report/system |
| entity_id | VARCHAR(100) | Required |
| event_timestamp | DATETIME(6) | Convert offset-aware values to UTC |
| ip_address | VARCHAR(45) NULL | Validate IPv4/IPv6; blank becomes NULL |
| details_json | JSON | Must be a JSON object; canonicalized |

Destination adds `actor_type` to distinguish user and system events and `ingested_at` for ingestion tracking.
