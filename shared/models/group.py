
from shared.db.database_base import PosgtreBase
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship

class Group(PosgtreBase):
    __tablename__ = "groups"

    id = Column("id", Integer, primary_key = True)

    level = Column("level", String(255))
    status = Column("status", Integer, nullable=False, default="0")
    
    style_id = Column("style_id", Integer, ForeignKey('styles.id'))
    style = relationship("Style", back_populates="groups", lazy="joined")
    
    teacher_id = Column("teacher_id", Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", back_populates="groups", lazy="joined")

    schedules = relationship("Schedule", back_populates="group")
    visits = relationship("Visit", back_populates="group")