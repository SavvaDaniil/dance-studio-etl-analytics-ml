import pandas as pd
from pandas import DataFrame
from datetime import date, datetime, timezone
from pathlib import Path

from src.extract.extract_abonements import extract_abonements
from src.extract.load_schedule import load_schedule
from src.extract.load_visits import load_visits
from src.extract.load_group_singles import load_group_singles

def save_raw(df: DataFrame, entity_name: str, ingested_at: datetime) -> None:
    #extract_date: date = ingested_at.date()
    extract_date_str: str = ingested_at.strftime("%Y-%m-%d")
    parquet_path: Path = Path(f"data/raw/{entity_name}/{extract_date_str}")
    parquet_path.mkdir(parents=True, exist_ok=True)
    df["_ingested_at"] = ingested_at
    df.to_parquet(f"{parquet_path}/{entity_name}.parquet", index=False)


def extract(extract_at: datetime, visit_date_from: datetime, visit_date_to: datetime):
    #today: date = date.today()
    #ingested_at = datetime.now(timezone.utc)


    branch_group_accounts_and_singles: dict[str, list] = extract_abonements()

    # Групповые абонементы
    df_groupAccountTypes: DataFrame = DataFrame(branch_group_accounts_and_singles["groupAccountTypes"])
    save_raw(df=df_groupAccountTypes, entity_name="groupAccountTypes", ingested_at=extract_at)

    # Разовые покупки и посещения
    df_groupSingleTypes: DataFrame = DataFrame(branch_group_accounts_and_singles["groupSingleTypes"])
    save_raw(df=df_groupSingleTypes, entity_name="groupSingleTypes", ingested_at=extract_at)



    
    # schedule 1-7 - monday-sunday
    schedules: list = load_schedule()
    #df_schedules["group_id"] = df_schedules["group"]["id"]

    styles_dict: dict[int, dict] = {}
    teachers_dict: dict[int, dict] = {}
    groups_dict: dict[int, dict] = {}

    for schedule in schedules:

        if schedule["group"] is None:
            continue

        if schedule["group"]["style"]["id"] not in styles_dict:
            styles_dict[schedule["group"]["style"]["id"]] = schedule["group"]["style"]
        #schedule["group"]["style_id"] = schedule["group"]["style"]["id"]

        if schedule["group"]["teacher1"]["id"] not in teachers_dict:
            teachers_dict[schedule["group"]["teacher1"]["id"]] = schedule["group"]["teacher1"]
        #schedule["group"]["teacher1_id"] = schedule["group"]["teacher1"]["id"]

        if schedule["group"]["id"] not in groups_dict:
            groups_dict[schedule["group"]["id"]] = schedule["group"]
        #schedule["group_id"] = schedule["group"]["id"]

    df_schedules: DataFrame = DataFrame(schedules)
    #print(df_schedules[df_schedules["dateBegin"].isna() | df_schedules["dateEnd"].isna()])
    #df_schedules["dateBegin"] = df_schedules["dateBegin"].astype(int)
    #df_schedules["dateEnd"] = df_schedules["dateEnd"].astype(int)
    #df_schedules.dropna()
    #print(df_schedules[df_schedules["day"].isna()])
    #df_schedules["day"].dropna()
    df_schedules = df_schedules.dropna(subset=["day"])
    #print(df_schedules.shape)
    df_schedules["day"] = df_schedules["day"].astype(int) # API returns mixed types ("8-11 лет", 18), keep as string in RAW layer.
    save_raw(df=df_schedules, entity_name="schedules", ingested_at=extract_at)

    df_styles: DataFrame = DataFrame(list(styles_dict.values()))
    save_raw(df=df_styles, entity_name="styles", ingested_at=extract_at)

    df_teachers: DataFrame = DataFrame(list(teachers_dict.values()))
    save_raw(df=df_teachers, entity_name="teachers", ingested_at=extract_at)

    df_groups: DataFrame = DataFrame(list(groups_dict.values()))
    df_groups["age"] = df_groups["age"].astype(str)
    save_raw(df=df_groups, entity_name="groups", ingested_at=extract_at)



    group_singles: list = load_group_singles(visit_date_from=int(visit_date_from.timestamp()), visit_date_to=int(visit_date_to.timestamp()))
    df_group_singles: DataFrame = DataFrame(group_singles)
    save_raw(df=df_group_singles, entity_name="group_singles", ingested_at=extract_at)


    # загрузка визитов
    #visit_date_from: int = int((datetime(2026, 1, 1)).timestamp())
    #visit_date_to: int = int((datetime.now()).timestamp())
    visits: list = load_visits(visit_date_from=int(visit_date_from.timestamp()), visit_date_to=int(visit_date_to.timestamp()))
    df_visits: DataFrame = DataFrame(visits)

    save_raw(df=df_visits, entity_name="visits", ingested_at=extract_at)


if __name__ == "__main__":
    extract(extract_at=datetime.now(timezone.utc), visit_date_from=datetime(2026, 1, 1), visit_date_to=date(2026, 7, 1))