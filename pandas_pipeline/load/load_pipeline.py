
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from datetime import datetime, date
from shared.db.database_session import get_engine
from shared.db.database_base import PosgtreBase
from sqlalchemy import text
from shared.models.style import Style
from shared.models.teacher import Teacher
from shared.models.group import Group
from shared.models.schedule import Schedule
from shared.models.group_single import GroupSingle
from shared.models.visit import Visit

def load(extract_at: datetime) -> None:
    extract_at_str: str = extract_at.strftime("%Y-%m-%d")
    
    df_styles: DataFrame = pd.read_parquet(f'./data/staging/styles/{extract_at_str}/styles.parquet')
    df_teachers: DataFrame = pd.read_parquet(f'./data/staging/teachers/{extract_at_str}/teachers.parquet')
    df_groups: DataFrame = pd.read_parquet(f'./data/staging/groups/{extract_at_str}/groups.parquet')
    df_schedules: DataFrame = pd.read_parquet(f'./data/staging/schedules/{extract_at_str}/schedules.parquet')
    df_group_singles: DataFrame = pd.read_parquet(f'./data/staging/group_singles/{extract_at_str}/group_singles.parquet')
    df_visits: DataFrame = pd.read_parquet(f'./data/staging/visits/{extract_at_str}/visits.parquet')

    engine = get_engine()
    PosgtreBase.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE styles CASCADE"))
        conn.execute(text("TRUNCATE TABLE teachers CASCADE"))
        conn.execute(text("TRUNCATE TABLE groups CASCADE"))
        conn.execute(text("TRUNCATE TABLE schedules CASCADE"))
        conn.execute(text("TRUNCATE TABLE group_singles CASCADE"))
        conn.execute(text("TRUNCATE TABLE visits CASCADE"))

    # load_styles
    df_styles.to_sql("styles", engine, if_exists="append", index=False)
    df_teachers.to_sql("teachers", engine, if_exists="append", index=False)
    df_groups.to_sql("groups", engine, if_exists="append", index=False)
    df_schedules.to_sql("schedules", engine, if_exists="append", index=False)
    df_group_singles.to_sql("group_singles", engine, if_exists="append", index=False)
    df_visits.to_sql("visits", engine, if_exists="append", index=False)



if __name__ == "__main__":
    load(extract_at=date(2026, 7, 27))