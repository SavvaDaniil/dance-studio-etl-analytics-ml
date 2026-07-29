
from pathlib import Path

import pandas as pd
import numpy as np
from pandas import DataFrame
from datetime import datetime, date

def get_season(month: int) -> str:
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    elif month in [9, 10, 11]:
        return 'autumn'

def save_staging(df: DataFrame, entity_name: str, extract_at_str: str) -> None:
    parquet_path: Path = Path(f"data/staging/{entity_name}/{extract_at_str}")
    parquet_path.mkdir(parents=True, exist_ok=True)
    df.to_parquet(f"{parquet_path}/{entity_name}.parquet", index=False)


def transform(extract_at: datetime):
    extract_at_str: str = extract_at.strftime("%Y-%m-%d")

    df_styles: DataFrame = pd.read_parquet(f'./data/raw/styles/{extract_at_str}/styles.parquet')
    #print(df_styles.info())
    df_styles = df_styles.drop(columns=["_ingested_at", "entity", "fotoFileName", "fotoUrl", "fotoThumbUrl"])
    #print(df_styles.head())
    #print(f"df_styles.shape: {df_styles.shape}")

    
    df_teachers: DataFrame = pd.read_parquet(f'./data/raw/teachers/{extract_at_str}/teachers.parquet')
    df_teachers = df_teachers.rename(columns={"lastName" : "last_name"})
    df_teachers = df_teachers.drop(columns=["_ingested_at", "rating", "address", "annotation", "inn", "post", "reviews", "birthDate", "email", "socialPage", "entity", "fotoFileName", "fotoUrl", "fotoThumbUrl", "phone", "middleName", "age", "man"])
    #print(df_teachers.head())
    #print(f"df_teachers.shape: {df_teachers.shape}")

    
    df_groups: DataFrame = pd.read_parquet(f'./data/raw/groups/{extract_at_str}/groups.parquet')
    df_groups["teacher_id"] = df_groups["teacher1"].str["id"]
    df_groups["style_id"] = df_groups["style"].str["id"]
    #df_groups["level"] = df_groups["level"].fillna("Общий")
    df_groups = df_groups.drop(columns=["_ingested_at", "age", "number", "placeCount", "showInWidget", "teacher2", "entity", "annotation", "style", "teacher1"])
    #print(df_groups.head())
    #print(f"df_groups.shape: {df_groups.shape}")


    df_schedules: DataFrame = pd.read_parquet(f'./data/raw/schedules/{extract_at_str}/schedules.parquet')
    df_schedules["group_id"] = df_schedules["group"].str["id"]
    df_schedules = df_schedules.rename(columns={"minutesBegin" : "minutes_begin", "minutesEnd" : "minutes_end"})
    df_schedules = df_schedules.drop(columns=["group", "target", "branch", "teacher", "teacher1", "teacher2", "style", "entity", "client", "date", "regular", "created", "creator", "hall", "color", "type", "note", "payment", "wage", "typeTitle", "deleted", "_ingested_at", "dateBegin", "dateEnd"])
    #print(df_schedules.info())
    #print(df_schedules.head())


    df_group_singles: DataFrame = pd.read_parquet(f'./data/raw/group_singles/{extract_at_str}/group_singles.parquet')
    #print(df_group_singles[['id','minutesEnd', "group"]])
    df_group_singles["group_id"] = df_group_singles["group"].str["id"]
    #print(df_group_singles[df_group_singles["minutesEnd"].isna()][['id','minutesEnd', "group_id"]])
    df_group_singles["style_id"] = df_group_singles["group"].str["style"].str["id"]
    df_group_singles["teacher_id"] = df_group_singles["group"].str["teacher1"].str["id"]
    df_group_singles["client_id"] = df_group_singles["client"].str["id"]
    #print(df_group_singles[df_group_singles['minutesEnd'].isna()])
    df_group_singles["visit_date"] = pd.to_datetime(df_group_singles["visitDate"], unit="s")
    df_group_singles["month"] = df_group_singles["visit_date"].dt.month
    df_group_singles["weekday"] = df_group_singles["visit_date"].dt.weekday
    df_group_singles["is_weekend"] = (df_group_singles["weekday"] > 4)
    df_group_singles["season"] = df_group_singles["month"].map(get_season)
    df_group_singles["quarter"] = df_group_singles["visit_date"].dt.quarter
    df_group_singles = df_group_singles.rename(columns={
        "typeName" : "type_name",
        "minutesBegin" : "minutes_begin", 
        "minutesEnd" : "minutes_end"
    })
    df_group_singles = df_group_singles.drop(columns=["_ingested_at", "id", "group", "target", "entity", "branch", "hall", "group", "archived", "annotation", "device", "deleted", "creator", "free", "service", "typeColor", "updated", "updater", "created", "shift", "clientOrder", "client", "visitDate", "duration", "payBox", "discount", "discountCurrency", "debt", "refund", "total", "paid"])
    #print(df_group_singles.head())


    df_visits: DataFrame = pd.read_parquet(f'./data/raw/visits/{extract_at_str}/visits.parquet')
    #print(df_visits.info())
    df_visits["group_id"] = df_visits["group"].str["id"]
    df_visits["teacher_id"] = df_visits["group"].str["teacher1"].str["id"]
    df_visits["client_id"] = df_visits["client"].str["id"]
    #df_visits["teacher_full_name"] = df_visits["group"].str["teacher1"].str["lastName"].str.strip() + " " + df_visits["group"].str["teacher1"].str["name"].str.strip()
    df_visits["style_id"] = df_visits["group"].str["style"].str["id"]
    #df_visits["style_name"] = df_visits["group"].str["style"].str["name"].str.strip()
    df_visits = df_visits.rename(columns={"minutesBegin" : "minutes_begin", "minutesEnd" : "minutes_end"})
    df_visits["visit_date"] = pd.to_datetime(df_visits["visitDate"], unit="s")
    df_visits["month"] = df_visits["visit_date"].dt.month
    df_visits["weekday"] = df_visits["visit_date"].dt.weekday
    df_visits["is_weekend"] = (df_visits["weekday"] > 4)
    df_visits["season"] = df_visits["month"].map(get_season)
    df_visits["quarter"] = df_visits["visit_date"].dt.quarter
    df_visits["group_account_id"] = df_visits["groupAccount"].str["id"]
    df_visits["group_account_cost"] = df_visits["groupAccount"].str["cost"]
    df_visits["group_account_trainings_total"] = df_visits["groupAccount"].str["trainingsTotal"]
    df_visits["group_account_is_unlimited"] = (df_visits["groupAccount"].str["trainingsTotal"] == -1)
    #df_visits["groupAccountTrainingsTotal"] = df_visits["groupAccount"].str["trainingsTotal"]
    #df_visits["lesson_cost"] = df_visits["groupAccount"].str["cost"] / df_visits["groupAccount"].str["trainingsTotal"]
    df_visits["lesson_cost"] = np.where(
        df_visits["groupAccount"].str["trainingsTotal"] > 0,
        df_visits["groupAccount"].str["cost"] /
        df_visits["groupAccount"].str["trainingsTotal"],
        None
    )

    df_visits = df_visits.drop(columns=["_ingested_at", "id", "free", "type", "burned", "entity", "_ingested_at", "client", "branch", "creator", "deleted", "target", "created", "cost", "service", "teacher", "hall", "rentAccount", "individualAccount", "selfAccount", "group", "visitDate", "duration", "groupAccount"])
    #print(df_visits[df_visits["deleted"].notna()]) #empty
    #print(df_visits[df_visits["duration"] != 60])
    #print(df_visits[df_visits["groupAccount"].isna()])
    #print(df_visits.head())

    # for df in [df_styles, df_teachers, df_groups, df_schedules, df_group_singles, df_visits]:
    #     print(df.head())

    save_staging(df=df_styles, entity_name="styles", extract_at_str=extract_at_str)
    save_staging(df=df_teachers, entity_name="teachers", extract_at_str=extract_at_str)
    save_staging(df=df_groups, entity_name="groups", extract_at_str=extract_at_str)
    save_staging(df=df_schedules, entity_name="schedules", extract_at_str=extract_at_str)
    save_staging(df=df_group_singles, entity_name="group_singles", extract_at_str=extract_at_str)
    save_staging(df=df_visits, entity_name="visits", extract_at_str=extract_at_str)
    
    

if __name__ == "__main__":
    transform(extract_at=date(2026, 7, 27))