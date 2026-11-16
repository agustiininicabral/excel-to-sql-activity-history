from __future__ import annotations
import ipaddress
import json
import re
from pathlib import Path
import pandas as pd

EMAIL=re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
EVENT_TYPES={"login","logout","create","update","delete","export","failed_login"}
ENTITY_TYPES={"auth","user","order","report","system"}

def _text(value):
    if pd.isna(value): return None
    value=str(value).strip()
    return value or None

def _utc_datetime(value):
    if value is None or pd.isna(value): return None
    parsed=pd.to_datetime(value,format="mixed",utc=True,errors="coerce")
    return None if pd.isna(parsed) else parsed.tz_convert(None).to_pydatetime()

def _ip(value):
    value=_text(value)
    if not value: return None
    return str(ipaddress.ip_address(value))

def _details(value):
    value=_text(value)
    parsed={} if not value else json.loads(value)
    if not isinstance(parsed,dict): raise ValueError("details_must_be_json_object")
    return json.dumps(parsed,sort_keys=True,separators=(",",":"))

def transform_workbook(path: str | Path):
    actors_raw=pd.read_excel(path,sheet_name="Actors",dtype=str)
    events_raw=pd.read_excel(path,sheet_name="ActivityEvents",dtype=str)
    actor_cols={"actor_user_id","email","display_name","is_active"}
    event_cols={"event_id","actor_user_id","event_type","entity_type","entity_id",
                "event_timestamp","ip_address","details_json"}
    if actor_cols-set(actors_raw.columns):
        raise ValueError(f"Actors sheet missing columns: {', '.join(sorted(actor_cols-set(actors_raw.columns)))}")
    if event_cols-set(events_raw.columns):
        raise ValueError(f"ActivityEvents sheet missing columns: {', '.join(sorted(event_cols-set(events_raw.columns)))}")

    actors=[]; actor_rejected=[]; seen_ids=set(); seen_emails=set()
    for row in actors_raw.to_dict("records"):
        raw_id=_text(row["actor_user_id"]); email=(_text(row["email"]) or "").lower()
        name=_text(row["display_name"]); active=(_text(row["is_active"]) or "").lower()
        reasons=[]
        try: uid=int(raw_id)
        except (TypeError,ValueError): uid=None; reasons.append("invalid_actor_user_id")
        if not email or not EMAIL.fullmatch(email): reasons.append("invalid_email")
        if not name: reasons.append("missing_display_name")
        if active not in {"0","1","true","false"}: reasons.append("invalid_is_active")
        if uid is not None and uid in seen_ids: reasons.append("duplicate_actor_user_id")
        if email and email in seen_emails: reasons.append("duplicate_actor_email")
        record={"actor_user_id":uid,"email":email,"display_name":name,
                "is_active":active in {"1","true"}}
        if reasons: actor_rejected.append({**record,"rejection_reason":"|".join(reasons)})
        else:
            seen_ids.add(uid); seen_emails.add(email); actors.append(record)
    actor_ids={r["actor_user_id"] for r in actors}

    events=[]; event_rejected=[]; seen_events=set()
    for row in events_raw.to_dict("records"):
        event_id=_text(row["event_id"])
        actor_ref=(_text(row["actor_user_id"]) or "").upper()
        event_type=(_text(row["event_type"]) or "").lower()
        entity_type=(_text(row["entity_type"]) or "").lower()
        entity_id=_text(row["entity_id"])
        timestamp=_utc_datetime(row["event_timestamp"])
        reasons=[]
        if not event_id: reasons.append("missing_event_id")
        if actor_ref=="SYSTEM": actor_id=None; actor_type="system"
        else:
            try: actor_id=int(actor_ref)
            except (TypeError,ValueError): actor_id=None
            actor_type="user"
            if actor_id not in actor_ids: reasons.append("unknown_actor")
        if event_type not in EVENT_TYPES: reasons.append("unsupported_event_type")
        if entity_type not in ENTITY_TYPES: reasons.append("unsupported_entity_type")
        if not entity_id: reasons.append("missing_entity_id")
        if not timestamp: reasons.append("invalid_event_timestamp")
        try: ip=_ip(row["ip_address"])
        except ValueError: ip=None; reasons.append("invalid_ip_address")
        try: details=_details(row["details_json"])
        except (ValueError,json.JSONDecodeError): details="{}"; reasons.append("invalid_details_json")
        if not reasons and event_id in seen_events: reasons.append("duplicate_event_id")
        record={"event_id":event_id,"actor_user_id":actor_id,"actor_type":actor_type,
                "event_type":event_type,"entity_type":entity_type,"entity_id":entity_id,
                "event_timestamp":timestamp,"ip_address":ip,"details_json":details}
        if reasons: event_rejected.append({**record,"rejection_reason":"|".join(reasons)})
        else:
            seen_events.add(event_id); events.append(record)
    accepted={"actors":pd.DataFrame(actors),"activity_logs":pd.DataFrame(events)}
    rejected={"actors":pd.DataFrame(actor_rejected),"activity_logs":pd.DataFrame(event_rejected)}
    return accepted,rejected,{"actors":len(actors_raw),"activity_logs":len(events_raw)}
