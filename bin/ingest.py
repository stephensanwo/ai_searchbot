from lib.io.ingest import convert_excel_to_json


def ingest_file(file_path: str) -> object:
    return convert_excel_to_json(file_path)
