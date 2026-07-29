
from sqlalchemy.orm import Session
from typing import Optional

from internal.models.visit import Visit

class VisitRepository:

    db: Session

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, id: int) -> Optional[Visit]:
        return self.db.query(Visit).filter(Visit.id == id).first()
    
    def add(self, obj: Visit) -> Visit:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj: Visit) -> None:
        self.db.query(Visit).filter(Visit.id == obj.id)\
            .update({
                Visit.minutes_begin : obj.minutes_begin,
                Visit.minutes_end : obj.minutes_end,
                Visit.group_id : obj.group_id,
                Visit.style_id : obj.style_id,
                Visit.style_name : obj.style_name,
                Visit.teacher_id : obj.teacher_id,
                Visit.teacher_full_name : obj.teacher_full_name,
                Visit.visit_date : obj.visit_date,
            }, synchronize_session = False)
        self.db.commit()