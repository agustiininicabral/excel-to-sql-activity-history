import mysql.connector
from activity_migration.config import DatabaseConfig

ACTOR_SQL="""INSERT INTO actors(actor_user_id,email,display_name,is_active) VALUES(%s,%s,%s,%s)
ON DUPLICATE KEY UPDATE email=VALUES(email),display_name=VALUES(display_name),is_active=VALUES(is_active)"""
EVENT_SQL="""INSERT INTO activity_logs
(event_id,actor_user_id,actor_type,event_type,entity_type,entity_id,event_timestamp,ip_address,details)
VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON DUPLICATE KEY UPDATE event_id=event_id"""

def load_all(accepted,config: DatabaseConfig):
    connection=mysql.connector.connect(host=config.host,port=config.port,database=config.database,
                                       user=config.user,password=config.password)
    try:
        cursor=connection.cursor()
        actor_values=[(r.actor_user_id,r.email,r.display_name,r.is_active)
                      for r in accepted["actors"].itertuples(index=False)]
        event_values=[(r.event_id,r.actor_user_id,r.actor_type,r.event_type,r.entity_type,r.entity_id,
                       r.event_timestamp,r.ip_address,r.details_json)
                      for r in accepted["activity_logs"].itertuples(index=False)]
        if actor_values: cursor.executemany(ACTOR_SQL,actor_values)
        if event_values: cursor.executemany(EVENT_SQL,event_values)
        connection.commit()
        return {"actors":len(actor_values),"activity_logs":len(event_values)}
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
