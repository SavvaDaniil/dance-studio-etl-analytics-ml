
from sqlalchemy.orm import Session
from typing import Optional

from internal.models.group import Group

class GroupRepository:

    db: Session

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, id: int) -> Optional[Group]:
        return self.db.query(Group).filter(Group.id == id).first()
    
    def add(self, obj: Group) -> Group:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj: Group) -> None:
        self.db.query(Group).filter(Group.id == obj.id)\
            .update({
                Group.level : obj.level,
                Group.status : obj.status,
                Group.style_id : obj.style_id,
                Group.teacher_id : obj.teacher_id,
            }, synchronize_session = False)
        self.db.commit()