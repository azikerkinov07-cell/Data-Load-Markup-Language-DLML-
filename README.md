# Data Load Markup Language (DLML)

DLML (Data Loading Markup Language) is a small learning project for describing
tables and their records in an XML-compatible format, then importing them into
SQLite.

## First prototype

The first version supports `TEXT`, `INTEGER`, and `REAL` columns. Each record
contains one `<field>` for every column. The importer creates a new SQLite
database file and adds the records from the DLML document.

Run that command from this directory.

## Installation

First, you need to clone the repository using the following command: `git clone git@github.com:azikerkinov07-cell/Data-Load-Markup-Language-DLML-.git` . Next, you need to run this command: `pipx install --force /path/DLML-Project`.

## Usage

To use this project, you first need to download it using the command provided above. To convert a .dlml file into a .db file (SQLite3), you should run the following command: `dlml users`. Note, however, that this will not work if you need to overwrite an existing file; for that purpose, the --overwrite flag is available: `dlml users --overwrite`

## Project layout

- `examples/users.dlml` — sample data file.
- `dlml.dtd` — document structure written as a DTD.
- `dlml/parser.py` — reads and validates DLML documents.
- `dlml/importer.py` — creates and fills a SQLite database.
- `dlml/cli.py` — command-line interface.

This prototype uses Python's XML parser, so DLML currently supports an
XML-compatible subset rather than every SGML feature.