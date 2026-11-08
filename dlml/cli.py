import argparse
from pathlib import Path

from .importer import import_database


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import a DLML file into SQLite"
    )
    parser.add_argument(
        "source",
        type=Path,
        help="path to a .dlml file, or its name without the extension",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="path for the output .db file (default: source name with .db extension)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="overwrite an existing database file",
    )

    args = parser.parse_args()

    source = args.source
    if not source.suffix:
        source = source.with_suffix(".dlml")

    output = args.output or source.with_suffix(".db")

    try:
        import_database(
            source,
            output,
            overwrite=args.overwrite,
        )
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))

    print(f"Database created: {output}")


if __name__ == "__main__":
    main()