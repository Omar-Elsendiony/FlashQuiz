from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Float
from sqlalchemy.orm import relationship


class QuizAttempt(BaseModel, Base):
    __tablename__ = 'quiz_attempt'

    quiz_id = Column(String(60), ForeignKey('quiz.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    score = Column(Float, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)

    user = relationship('User', back_populates='quiz_attempts')
    quiz = relationship('Quiz', back_populates='attempts')
    responses = relationship('QuizResponse', backref='attempt', lazy=True)
