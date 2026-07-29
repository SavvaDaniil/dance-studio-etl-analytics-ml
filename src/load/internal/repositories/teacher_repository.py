
from sqlalchemy.orm import Session
from typing import Optional

from internal.models.teacher import Teacher

class TeacherRepository:

    db: Session

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, id: int) -> Optional[Teacher]:
        return self.db.query(Teacher).filter(Teacher.id == id).first()
    
    def add(self, obj: Teacher) -> Teacher:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj: Teacher) -> None:
        self.db.query(Teacher).filter(Teacher.id == obj.id)\
            .update({
                Teacher.last_name : obj.last_name,
                Teacher.name : obj.name,
                Teacher.is_man : obj.is_man,
            }, synchronize_session = False)
        self.db.commit()