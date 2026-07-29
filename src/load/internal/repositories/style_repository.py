
from sqlalchemy.orm import Session
from typing import Optional

from internal.models.style import Style

class StyleRepository:

    db: Session

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, id: int) -> Optional[Style]:
        return self.db.query(Style).filter(Style.id == id).first()
    
    def add(self, obj: Style) -> Style:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, obj: Style) -> None:
        self.db.query(Style).filter(Style.id == obj.id)\
            .update({
                Style.name : obj.name,
            }, synchronize_session = False)
        self.db.commit()