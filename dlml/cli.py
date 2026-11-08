import argparse
from pathlib import Path

from .importer import import_database


def main() -> None:
    parser = argparse.ArgumentParser(description="Загрузить DLML-файл в SQLite")
    parser.add_argument("source", type=Path, help="путь к .dlml-файлу")
    parser.add_argument("--output", type=Path, required=True, help="куда сохранить .db")
    args = parser.parse_args()

    try:
        import_database(args.source, args.output)
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))
    print(f"База создана: {args.output}")
