from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Table
from sqlalchemy.orm import relationship



class Option(BaseModel, Base):
    __tablename__ = 'option'
    # id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    is_correct = Column(Boolean, default=False)
    
    question_id = Column(String(60), ForeignKey('question.id'), nullable=False)
    # question = relationship('Question', backref='options-question')

