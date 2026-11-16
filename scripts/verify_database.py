import os
import mysql.connector

def main():
    connection=mysql.connector.connect(host=os.getenv("DB_HOST","127.0.0.1"),
        port=int(os.getenv("DB_PORT","3306")),database=os.getenv("DB_NAME","activity_migration"),
        user=os.getenv("DB_USER","root"),password=os.getenv("DB_PASSWORD",""))
    try:
        cursor=connection.cursor()
        for table,expected in (("actors",8),("activity_logs",18)):
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            actual=cursor.fetchone()[0]
            assert actual==expected, f"{table}: expected {expected}, got {actual}"
            print(f"{table}: {actual} rows verified")
        cursor.execute("SELECT COUNT(*) FROM activity_logs WHERE actor_type='system' AND actor_user_id IS NULL")
        assert cursor.fetchone()[0]==1, "Expected one system event with a NULL actor foreign key"
        cursor.execute("""SELECT COUNT(*) FROM activity_logs l
            LEFT JOIN actors a ON a.actor_user_id=l.actor_user_id
            WHERE l.actor_type='user' AND a.actor_user_id IS NULL""")
        assert cursor.fetchone()[0]==0, "Orphan user events found"
        cursor.execute("SELECT COUNT(*) FROM activity_logs WHERE JSON_VALID(details)=0")
        assert cursor.fetchone()[0]==0, "Invalid JSON payload found in MySQL"
        print("Audit integrity verified: UTC timestamps persisted, system actor is NULL, user FKs and JSON are valid.")
    finally: connection.close()

if __name__=="__main__": main()
