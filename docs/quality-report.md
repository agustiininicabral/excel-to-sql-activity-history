# Sample quality report

The synthetic workbook contains 8 actors and 25 activity events.

Expected dry-run result:
- Actors: 8 accepted, 0 rejected.
- Activity events: 18 accepted, 7 rejected.

The rejected examples cover a repeated event ID, unknown actor, invalid timestamp, unsupported event type, invalid IP address, malformed JSON payload, and missing entity ID. The accepted + rejected totals reconcile to the source counts.

All timestamps are stored as UTC after parsing. The naive sample timestamp is explicitly assumed to be UTC; production migrations must validate this assumption with the source system owner.
