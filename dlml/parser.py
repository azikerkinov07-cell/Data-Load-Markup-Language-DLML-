from dataclasses import dataclass
from pathlib import Path
import re
import xml.etree.ElementTree as ET


SUPPORTED_TYPES = {"TEXT", "INTEGER", "REAL"}
IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass
class Column:
    name: str
    data_type: str
    primary_key: bool


@dataclass
class Table:
    name: str
    columns: list[Column]
    records: list[list[str]]


def parse_document(path: Path) -> list[Table]:
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as error:
        raise ValueError(f"Could not read DLML file: {error}") from error

    if root.tag != "database":
        raise ValueError("The root element must be <database>")

    tables = []
    for table_element in root:
        if table_element.tag != "table":
            raise ValueError("Only <table> elements are allowed inside <database>")

        table_name = _identifier(table_element.get("name"), "table name")
        columns = []
        records = []
        reading_records = False

        for child in table_element:
            if child.tag == "column" and not reading_records:
                name = _identifier(child.get("name"), "column name")
                data_type = child.get("type", "").upper()
                if data_type not in SUPPORTED_TYPES:
                    raise ValueError(
                        f"Unknown type {data_type!r} for column {name!r}"
                    )
                primary_key = child.get("primary-key", "false") == "true"
                columns.append(Column(name, data_type, primary_key))
            elif child.tag == "record":
                reading_records = True
                values = []
                for field in child:
                    if field.tag != "field":
                        raise ValueError(
                            "Only <field> elements are allowed inside <record>"
                        )
                    values.append(field.text or "")
                records.append(values)
            else:
                raise ValueError(
                    "Inside <table>, place <column> elements before <record> elements"
                )

        if not columns:
            raise ValueError(f"Table {table_name!r} has no columns")
        if len({column.name for column in columns}) != len(columns):
            raise ValueError(f"Duplicate column names in table {table_name!r}")
        if sum(column.primary_key for column in columns) > 1:
            raise ValueError("Only one primary key is supported in this version")

        for record_number, values in enumerate(records, start=1):
            if len(values) != len(columns):
                raise ValueError(
                    f"Record {record_number} in table {table_name!r}: "
                    f"expected {len(columns)} fields, got {len(values)}"
                )

        tables.append(Table(table_name, columns, records))

    if not tables:
        raise ValueError("The document must contain at least one table")
    if len({table.name for table in tables}) != len(tables):
        raise ValueError("Duplicate table names in the document")

    return tables


def _identifier(value: str | None, label: str) -> str:
    if value is None or not IDENTIFIER.fullmatch(value):
        raise ValueError(f"Invalid {label}: {value!r}")
    return value