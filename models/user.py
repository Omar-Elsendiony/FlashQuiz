import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Table
from sqlalchemy.orm import relationship



class User(BaseModel, Base):
    __tablename__ = 'user'
    # id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128))
    
    quizzes = relationship('Quiz', backref='creator-quiz')
    flashcards = relationship('Flashcard', backref='creator-flashcard')
    favorite_quizzes = relationship('Quiz', secondary='user_favorite_quizzes', backref='favorited_by-quizzes')
    favorite_flashcards = relationship('Flashcard', secondary='user_favorite_flashcards', backref='favorited_by-flashcards')


# Association tables for many-to-many relationships
user_favorite_quizzes = Table('user_favorite_quizzes',
                              Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('quiz_id', Integer, ForeignKey('quiz.id'), primary_key=True)
)

user_favorite_flashcards = Table('user_favorite_flashcards',
                                 Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('flashcard_id', Integer, ForeignKey('flashcard.id'), primary_key=True)
)

