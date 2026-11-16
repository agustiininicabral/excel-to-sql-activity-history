# Sample quality report

The synthetic workbook contains 8 actors and 25 activity events.

Expected dry-run result:
- Actors: 8 accepted, 0 rejected.
- Activity events: 18 accepted, 7 rejected.

The rejected examples cover a repeated event ID, unknown actor, invalid timestamp, unsupported event type, invalid IP address, malformed JSON payload, and missing entity ID. The accepted + rejected totals reconcile to the source counts.

All timestamps are stored as UTC after parsing. The naive sample timestamp is explicitly assumed to be UTC; production migrations must validate this assumption with the source system owner.


## Database integration

The CI run performs a real load into a disposable MySQL 8.0 service and verifies 8 actors, 18 events, one system event with a NULL actor foreign key, valid JSON payloads, and no orphan user references. No production data or database is used.
