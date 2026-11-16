from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/source/activity_history.xlsx"
ACTORS=[
[1,"ana.garcia@example.com","Ana García",1],[2,"bruno.perez@example.com","Bruno Pérez",1],
[3,"carla.lopez@example.com","Carla López",1],[4,"diego.fernandez@example.com","Diego Fernández",1],
[5,"elena.suarez@example.com","Elena Suárez",1],[6,"facundo.romero@example.com","Facundo Romero",1],
[7,"gabriela.torres@example.com","Gabriela Torres",1],[8,"hugo.diaz@example.com","Hugo Díaz",0]]
EVENTS=[
["EVT-001",1,"login","auth","session-001","2025-01-01T09:00:00-03:00","192.0.2.10",'{"method":"password","success":true}'],
["EVT-002",2,"login","auth","session-002","2025-01-01T09:05:00Z","192.0.2.11",'{"method":"sso","success":true}'],
["EVT-003",3,"create","user","user-203","2025-01-02 10:15:00","198.51.100.20",'{"source":"admin_panel"}'],
["EVT-004",4,"update","order","order-5001","2025-01-02T13:20:00-03:00","198.51.100.21",'{"field":"status","from":"new","to":"paid"}'],
["EVT-005",5,"export","report","report-sales-q1","2025-01-03T12:30:00Z","203.0.113.5",'{"format":"csv","rows":250}'],
["EVT-006",6,"failed_login","auth","session-006","2025-01-03T09:45:00-03:00","203.0.113.6",'{"reason":"invalid_password"}'],
["EVT-007",7,"logout","auth","session-007","2025-01-04T17:00:00Z","192.0.2.15",'{"duration_seconds":3600}'],
["EVT-008",8,"login","auth","session-008","2025-01-05T08:30:00-03:00","192.0.2.16",'{"method":"password","success":true}'],
["EVT-009",1,"update","user","user-101","2025-01-05T11:12:00Z","192.0.2.10",'{"field":"email"}'],
["EVT-010",2,"delete","order","order-4002","2025-01-06T14:10:00-03:00","192.0.2.11",'{"reason":"duplicate"}'],
["EVT-011",3,"create","order","order-5002","2025-01-07T12:00:00Z","198.51.100.20",'{"items":3}'],
["EVT-012",4,"update","report","report-77","2025-01-08T15:22:00-03:00","198.51.100.21",'{"field":"title"}'],
["EVT-013",5,"export","report","report-78","2025-01-09T16:00:00Z","203.0.113.5",'{"format":"xlsx","rows":80}'],
["EVT-014",6,"login","auth","session-014","2025-01-10T07:00:00-03:00","203.0.113.6",'{"method":"sso","success":true}'],
["EVT-015",7,"logout","auth","session-015","2025-01-10T19:00:00Z","192.0.2.15",'{"duration_seconds":4200}'],
["EVT-016",1,"failed_login","auth","session-016","2025-01-11T09:10:00-03:00","192.0.2.10",'{"reason":"mfa_timeout"}'],
["EVT-017",2,"create","user","user-204","2025-01-12T12:00:00Z","192.0.2.11",'{"source":"api"}'],
["EVT-018","SYSTEM","update","system","maintenance-01","2025-01-13T02:00:00Z","",'{"task":"scheduled_maintenance"}'],
["EVT-001",1,"login","auth","session-001","2025-01-01T09:00:00-03:00","192.0.2.10",'{"method":"password","success":true}'],
["EVT-020",999,"login","auth","session-020","2025-01-14T09:00:00Z","192.0.2.99",'{"method":"password"}'],
["EVT-021",3,"update","order","order-5003","not-a-timestamp","198.51.100.20",'{"field":"status"}'],
["EVT-022",4,"grant_admin","user","user-300","2025-01-15T10:00:00Z","198.51.100.21",'{"role":"admin"}'],
["EVT-023",5,"export","report","report-79","2025-01-16T10:00:00Z","999.999.999.999",'{"format":"csv"}'],
["EVT-024",6,"update","order","order-5004","2025-01-17T11:00:00Z","203.0.113.6",'{"field":broken}'],
["EVT-025",7,"delete","order","","2025-01-18T11:00:00Z","192.0.2.15",'{"reason":"requested"}']]
def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with pd.ExcelWriter(OUT,engine="openpyxl") as writer:
        pd.DataFrame(ACTORS,columns=["actor_user_id","email","display_name","is_active"]).to_excel(writer,sheet_name="Actors",index=False)
        pd.DataFrame(EVENTS,columns=["event_id","actor_user_id","event_type","entity_type","entity_id","event_timestamp","ip_address","details_json"]).to_excel(writer,sheet_name="ActivityEvents",index=False)
    print(f"Generated {OUT}: {len(ACTORS)} actors and {len(EVENTS)} activity events")
if __name__=="__main__": main()
