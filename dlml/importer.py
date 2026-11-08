import sqlite3
from pathlib import Path

from .parser import Table, parse_document


def import_database(
    source: Path,
    output: Path,
    overwrite: bool = False,
) -> None:
    tables = parse_document(source)

    if output.exists():
        if not overwrite:
            raise FileExistsError(f"Database file already exists: {output}")
        output.unlink()

    try:
        with sqlite3.connect(output) as connection:
            for table in tables:
                _create_table(connection, table)
                _insert_records(connection, table)
    except Exception:
        output.unlink(missing_ok=True)
        raise


def _create_table(connection: sqlite3.Connection, table: Table) -> None:
    definitions = []
    for column in table.columns:
        definition = f'"{column.name}" {column.data_type}'
        if column.primary_key:
            definition += " PRIMARY KEY"
        definitions.append(definition)

    sql = f'CREATE TABLE "{table.name}" ({", ".join(definitions)})'
    connection.execute(sql)


def _insert_records(connection: sqlite3.Connection, table: Table) -> None:
    if not table.records:
        return

    column_names = ", ".join(f'"{column.name}"' for column in table.columns)
    placeholders = ", ".join("?" for _ in table.columns)
    sql = f'INSERT INTO "{table.name}" ({column_names}) VALUES ({placeholders})'

    converted_records = [
        [
            _convert_value(value, column.data_type)
            for value, column in zip(record, table.columns)
        ]
        for record in table.records
    ]
    connection.executemany(sql, converted_records)


def _convert_value(value: str, data_type: str):
    try:
        if data_type == "INTEGER":
            return int(value)
        if data_type == "REAL":
            return float(value)
    except ValueError as error:
        raise ValueError(
            f"Value {value!r} is not valid for type {data_type}"
        ) from error

    return value