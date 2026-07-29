
from src.load.internal.db.database_base import PosgtreBase
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship

class Style(PosgtreBase):
    __tablename__ = "styles"

    id = Column("id", Integer, primary_key = True)
    name = Column("name", String(255))
    
    groups = relationship("Group", back_populates="style")
    visits = relationship("Visit", back_populates="style")