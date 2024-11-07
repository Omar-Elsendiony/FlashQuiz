from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Table
from sqlalchemy.orm import relationship

class QuizResponse(BaseModel, Base):
    attempt_id = Column(String(60), ForeignKey('quiz_attempt.id'), nullable=False)
    question_id = Column(String(60), ForeignKey('question.id'), nullable=False)
    submitted_answer = Column(String(255), nullable=False)
    is_correct = Column(Boolean, nullable=False)
