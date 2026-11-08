# DLML

DLML (Data Loading Markup Language) is a small learning project for describing
tables and their records in an XML-compatible format, then importing them into
SQLite.

## First prototype

The first version supports `TEXT`, `INTEGER`, and `REAL` columns. Each record
contains one `<field>` for every column. The importer creates a new SQLite
database file and adds the records from the DLML document.

```bash
python3 -m dlml examples/users.dlml --output users.db
```

Run that command from this directory.

## Project layout

- `examples/users.dlml` — sample data file.
- `dlml.dtd` — document structure written as a DTD.
- `dlml/parser.py` — reads and validates DLML documents.
- `dlml/importer.py` — creates and fills a SQLite database.
- `dlml/cli.py` — command-line interface.

This prototype uses Python's XML parser, so DLML currently supports an
XML-compatible subset rather than every SGML feature.
