from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Table
from sqlalchemy.orm import relationship



class Quiz(BaseModel, Base):
    __tablename__ = 'quiz'
    # id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    view_count = Column(Integer, default=0)
    creator_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    # creator = relationship('User', backref='quizz-creator')
    category_id = Column(String(60), ForeignKey('category.id'), nullable=False)
    
    
    category = relationship('Category', backref='quiz-category')
    questions = relationship('Question', backref='quiz-questions', cascade='all, delete-orphan')
    attempts = relationship('QuizAttempt', back_populates='quiz')


    favorited_by = relationship('User',
                                secondary='user_favorite_quizzes', 
                                back_populates='favorited_quizzes',
                                overlaps="favorited_by")
