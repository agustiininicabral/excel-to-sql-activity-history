# Migration design

1. Read the Actors and ActivityEvents worksheets.
2. Validate actor IDs, emails, names, and active flags.
3. Build the set of accepted actor IDs.
4. Normalize event identifiers, actor references, event/entity types, and entity IDs.
5. Convert timestamps with offsets to UTC. Naive timestamps are assumed UTC for this sample; this assumption must be confirmed with source owners in a real migration.
6. Validate IP addresses and parse details as JSON objects.
7. Reject events with unknown actors, duplicate IDs, invalid dates, unsupported types, invalid IPs/JSON, or missing entity IDs.
8. Export accepted/rejected reports and reconcile every source row.
9. Load actors first, then events, in one MySQL transaction. Existing event IDs are treated as immutable and are not overwritten.

## Audit integrity considerations

Historical events should be append-oriented. Do not silently rewrite timestamps or payloads to make an import pass. Preserve the source snapshot, document timezone assumptions, restrict update/delete privileges, define retention, and reconcile source and destination counts before cutover.
