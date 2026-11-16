CREATE DATABASE IF NOT EXISTS activity_migration CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE activity_migration;

CREATE TABLE IF NOT EXISTS actors (
 actor_user_id BIGINT UNSIGNED PRIMARY KEY,
 email VARCHAR(254) NOT NULL UNIQUE,
 display_name VARCHAR(160) NOT NULL,
 is_active BOOLEAN NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS activity_logs (
 event_id VARCHAR(40) PRIMARY KEY,
 actor_user_id BIGINT UNSIGNED NULL,
 actor_type VARCHAR(10) NOT NULL,
 event_type VARCHAR(30) NOT NULL,
 entity_type VARCHAR(30) NOT NULL,
 entity_id VARCHAR(100) NOT NULL,
 event_timestamp DATETIME(6) NOT NULL COMMENT 'UTC',
 ip_address VARCHAR(45) NULL,
 details JSON NOT NULL,
 ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CONSTRAINT fk_activity_actor FOREIGN KEY (actor_user_id) REFERENCES actors(actor_user_id) ON DELETE RESTRICT,
 CONSTRAINT chk_activity_actor_type CHECK (
   (actor_type='system' AND actor_user_id IS NULL) OR
   (actor_type='user' AND actor_user_id IS NOT NULL)
 ),
 CONSTRAINT chk_activity_event_type CHECK (event_type IN
   ('login','logout','create','update','delete','export','failed_login')),
 INDEX idx_activity_timestamp (event_timestamp),
 INDEX idx_activity_actor_time (actor_user_id,event_timestamp),
 INDEX idx_activity_event_type_time (event_type,event_timestamp)
) ENGINE=InnoDB;
