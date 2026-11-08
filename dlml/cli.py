import argparse
from pathlib import Path

from .importer import import_database


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import a DLML file into SQLite"
    )
    parser.add_argument("source", type=Path, help="path to the .dlml file")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="path for the output .db file",
    )
    args = parser.parse_args()

    try:
        import_database(args.source, args.output)
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))

    print(f"Database created: {args.output}")