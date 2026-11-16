from pathlib import Path
import subprocess,sys
from activity_migration.transform import transform_workbook

ROOT=Path(__file__).resolve().parents[1]

def test_sample_workbook_reconciles_and_rejects_bad_events():
    workbook=ROOT/"data/source/activity_history.xlsx"
    if not workbook.exists():
        subprocess.run([sys.executable,"scripts/generate_sample_workbook.py"],cwd=ROOT,check=True)
    accepted,rejected,counts=transform_workbook(workbook)
    assert len(accepted["actors"])==8
    assert len(rejected["actors"])==0
    assert len(accepted["activity_logs"])==18
    assert len(rejected["activity_logs"])==7
    assert len(accepted["activity_logs"])+len(rejected["activity_logs"])==counts["activity_logs"]
    reasons="|".join(rejected["activity_logs"].rejection_reason)
    for expected in ["duplicate_event_id","unknown_actor","invalid_event_timestamp",
                     "unsupported_event_type","invalid_ip_address","invalid_details_json","missing_entity_id"]:
        assert expected in reasons

def test_system_actor_is_preserved_without_user_foreign_key():
    workbook=ROOT/"data/source/activity_history.xlsx"
    if not workbook.exists():
        subprocess.run([sys.executable,"scripts/generate_sample_workbook.py"],cwd=ROOT,check=True)
    accepted,_,_=transform_workbook(workbook)
    system=accepted["activity_logs"].query("actor_type == 'system'")
    assert len(system)==1
    assert system.iloc[0].actor_user_id is None
