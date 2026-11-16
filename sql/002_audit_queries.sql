USE activity_migration;

-- Event volume by UTC day
SELECT DATE(event_timestamp) AS event_day_utc, COUNT(*) AS events
FROM activity_logs GROUP BY DATE(event_timestamp) ORDER BY event_day_utc;

-- Event type distribution
SELECT event_type, COUNT(*) AS events
FROM activity_logs GROUP BY event_type ORDER BY events DESC;

-- Most active actors
SELECT a.actor_user_id, a.display_name, COUNT(*) AS event_count
FROM actors a JOIN activity_logs l ON l.actor_user_id=a.actor_user_id
GROUP BY a.actor_user_id,a.display_name ORDER BY event_count DESC;

-- System-generated events
SELECT event_id,event_type,entity_type,entity_id,event_timestamp
FROM activity_logs WHERE actor_type='system' ORDER BY event_timestamp;

-- Must return zero: invalid actor references
SELECT COUNT(*) AS orphan_actor_events
FROM activity_logs l LEFT JOIN actors a ON a.actor_user_id=l.actor_user_id
WHERE l.actor_type='user' AND a.actor_user_id IS NULL;

-- Historical range
SELECT MIN(event_timestamp) AS first_event_utc, MAX(event_timestamp) AS last_event_utc
FROM activity_logs;
