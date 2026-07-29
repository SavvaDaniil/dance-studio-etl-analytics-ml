from datetime import date, datetime, timezone

from src.extract.extract_all_datas import extract
from src.transform.transform_all_pandas import transform
from src.load.load_all_pandas import load


def main(extract_at: datetime, visit_date_from: datetime, visit_date_to: datetime) -> None:

    print("Start extracting")
    extract(extract_at=extract_at, visit_date_from=visit_date_from, visit_date_to=visit_date_to)

    print("--- finish extract\nStart transforming")
    transform(extract_at=extract_at)

    print("--- finish transforming\nStart loading")
    load(extract_at=extract_at)

    print("--- finish loading")

if __name__ == "__main__":
    main(extract_at=datetime.now(timezone.utc), visit_date_from=datetime(2024, 1, 1), visit_date_to=datetime(2026, 7, 1))

# 2026 7 27