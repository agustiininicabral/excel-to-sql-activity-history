from datetime import datetime
import pytest
from activity_migration.transform import _utc_datetime,_ip,_details

def test_offset_timestamp_is_converted_to_utc():
    parsed=_utc_datetime("2025-01-01T09:00:00-03:00")
    assert parsed==datetime(2025,1,1,12,0,0)

def test_naive_timestamp_is_assumed_utc():
    parsed=_utc_datetime("2025-01-02 10:15:00")
    assert parsed==datetime(2025,1,2,10,15,0)

def test_ip_address_is_canonicalized():
    assert _ip("192.0.2.10")=="192.0.2.10"

def test_invalid_ip_is_rejected():
    with pytest.raises(ValueError): _ip("999.999.999.999")

def test_details_must_be_json_object():
    assert _details('{"b":2,"a":1}')=='{"a":1,"b":2}'
    with pytest.raises(ValueError): _details("[1,2]")
