
from src.load.internal.db.database_base import PosgtreBase
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship

class Teacher(PosgtreBase):
    __tablename__ = "teachers"

    id = Column("id", Integer, primary_key = True)

    last_name = Column("last_name", String(255))
    name = Column("name", String(255))
    #is_man = Column("is_man", Boolean, nullable=False, server_default=text("false"))
    
    groups = relationship("Group", back_populates="teacher")
    visits = relationship("Visit", back_populates="teacher")
    