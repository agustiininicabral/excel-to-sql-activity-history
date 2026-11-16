# Excel to SQL: Activity History Migration

[![CI](https://github.com/agustiininicabral/excel-to-sql-activity-history/actions/workflows/ci.yml/badge.svg)](https://github.com/agustiininicabral/excel-to-sql-activity-history/actions/workflows/ci.yml)

A reproducible practice project migrating synthetic audit and activity events from Excel into **MySQL 8.0**. It focuses on historical timestamp normalization, UTC conversion, actor referential integrity, event validation, duplicate handling, append-oriented loading, and audit queries.

> Educational portfolio project. All actors and events are synthetic. This is not a production audit-log platform.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/generate_sample_workbook.py
```

Validate without connecting to MySQL:

```bash
PYTHONPATH=src python -m activity_migration.main --dry-run --input data/source/activity_history.xlsx
```

Create the schema and load:

```bash
mysql -u root -p < sql/001_create_schema.sql
# Copy .env.example to .env and configure local credentials.
PYTHONPATH=src python -m activity_migration.main --input data/source/activity_history.xlsx
```

## Migration rules

- Normalize event IDs, event types, entity references, and actor IDs.
- Convert timestamps with offsets to UTC before storing them as UTC `DATETIME(6)`.
- Treat naive timestamps as UTC for this synthetic source; a real source must document its timezone.
- Accept a `SYSTEM` actor as a null user foreign key with actor type `system`.
- Reject unknown actors, malformed timestamps, unsupported event types, invalid IP addresses, malformed JSON, missing entity IDs, and duplicate event IDs.
- Keep audit events immutable on repeated loads; duplicate event IDs do not overwrite the original event.

## Contents

`data/` sample Excel workbook; `src/` parsing, validation, and MySQL loader; `sql/` schema and audit queries; `tests/` automated checks; `docs/` data dictionary, design, quality report, and diagrams.

Run `pytest`. GitHub Actions regenerates the workbook, runs tests and a dry-run, then uploads accepted/rejected reports as a workflow artifact.

## Limitations

Small synthetic sample with a single source timezone assumption for naive timestamps. A production audit trail requires immutable storage policy, access controls, retention policy, tamper-evidence, time-source governance, monitoring, and legal/security review.
