import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Table
from sqlalchemy.orm import relationship
from hashlib import md5
from flask_login import UserMixin

class User(BaseModel, Base, UserMixin):
    __tablename__ = 'user'
    # id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128))
    
    quizzes = relationship('Quiz', backref='creator-quiz')
    flashcards = relationship('Flashcard', backref='creator-flashcard')

    favorited_quizzes = relationship('Quiz', 
                                    secondary='user_favorite_quizzes', 
                                    back_populates='favorited_by')
    
    favorited_flashcards = relationship('Flashcard', 
                                        secondary='user_favorite_flashcards', 
                                        back_populates='favorited_by')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

# Association tables for many-to-many relationships
user_favorite_quizzes = Table('user_favorite_quizzes',
                            Base.metadata,
    Column('user_id', String(60), ForeignKey('user.id'), primary_key=True),
    Column('quiz_id', String(60), ForeignKey('quiz.id'), primary_key=True)
)

user_favorite_flashcards = Table('user_favorite_flashcards',
                                Base.metadata,
    Column('user_id', String(60), ForeignKey('user.id'), primary_key=True),
    Column('flashcard_id', String(60), ForeignKey('flashcard.id'), primary_key=True)
)

