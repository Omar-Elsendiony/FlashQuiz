from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Table
from sqlalchemy.orm import relationship




class Question(BaseModel, Base):
    __tablename__ = 'question'
    # id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    question_type = Column(String(20), nullable=False)  # 'mcq' or 'true-false'
    
    quiz_id = Column(String(60), ForeignKey('quiz.id'), nullable=False)
    # quiz = relationship('Quiz', backref='questions-quiz')
    
    options = relationship('Option', backref='question-options', cascade='all, delete-orphan')

