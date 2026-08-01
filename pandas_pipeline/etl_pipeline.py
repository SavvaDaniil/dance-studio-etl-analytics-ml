from datetime import date, datetime, timezone

from shared.extract.extract_pipeline import extract
from pandas_pipeline.transform.transform_pipeline import transform
from pandas_pipeline.load.load_pipeline import load


def main(extract_at: datetime, visit_date_from: datetime, visit_date_to: datetime) -> None:

    print("Start extracting")
    extract(extract_at=extract_at, visit_date_from=visit_date_from, visit_date_to=visit_date_to)

    print("--- finish extract\nStart transforming")
    transform(extract_at=extract_at)

    print("--- finish transforming\nStart loading")
    load(extract_at=extract_at)

    print("--- finish loading")

if __name__ == "__main__":
    main(
        extract_at=datetime(2026, 8, 1), #datetime.now(timezone.utc), 
        visit_date_from=datetime(2026, 6, 1), 
        visit_date_to=datetime(2026, 8, 1)
    )

# 2026 7 29 - 6 months