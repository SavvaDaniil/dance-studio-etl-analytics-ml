
from sqlalchemy.orm import Session
from typing import Optional

from internal.models.schedule import Schedule

class ScheduleRepository:

    db: Session

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, id: int) -> Optional[Schedule]:
        return self.db.query(Schedule).filter(Schedule.id == id).first()
    
    def add(self, obj: Schedule) -> Schedule:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj: Schedule) -> None:
        self.db.query(Schedule).filter(Schedule.id == obj.id)\
            .update({
                Schedule.day : obj.day,
                Schedule.group_id : obj.group_id,
                Schedule.minutes_begin : obj.minutes_begin,
                Schedule.minutes_end : obj.minutes_end,
            }, synchronize_session = False)
        self.db.commit()