
from src.load.internal.db.database_base import PosgtreBase
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship

class Schedule(PosgtreBase):
    __tablename__ = "schedules"

    id = Column("id", Integer, primary_key = True)

    day = Column("day", Integer, nullable=False, default="0")
    
    group_id = Column("group_id", Integer, ForeignKey('groups.id'))
    group = relationship("Group", back_populates="schedules", lazy="joined")

    minutes_begin = Column("minutes_begin", Integer, nullable=False, default="0")
    minutes_end = Column("minutes_end", Integer, nullable=False, default="0")