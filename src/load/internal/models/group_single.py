
from src.load.internal.db.database_base import PosgtreBase
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, text
from sqlalchemy.orm import relationship

class GroupSingle(PosgtreBase):
    __tablename__ = "group_singles"

    id = Column("id", Integer, primary_key = True)

    type_name = Column("type_name", String(255))
    #duration = Column("duration", Integer, nullable=False, default="0")
    minutes_begin = Column("minutes_begin", Integer, nullable=True, default="0")
    minutes_end = Column("minutes_end", Integer, nullable=True, default="0")
    
    group_id = Column("group_id", Integer, ForeignKey('groups.id'))
    group = relationship("Group", back_populates="visits", lazy="joined")
    
    style_id = Column("style_id", Integer, ForeignKey('styles.id'))
    style = relationship("Style", back_populates="visits", lazy="joined")
    #style_name = Column("style_name", String(255))
    
    teacher_id = Column("teacher_id", Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", back_populates="visits", lazy="joined")
    #teacher_full_name = Column("teacher_full_name", String(255))

    client_id = Column("client_id", Integer, nullable=False, default="0")
    cost = Column("cost", Integer, nullable=False, default="0")

    visit_date = Column("visit_date", Date, nullable=True)
    month = Column("month", Integer, nullable=False, default="0")
    weekday = Column("weekday", Integer, nullable=False, default="0")
    is_weekend = Column("is_weekend", Boolean, nullable=False, server_default=text("false"))
    season = Column("season", String(255))
    quarter = Column("quarter", Integer, nullable=False, default="0")
