#!/usr/bin/python3
"""
Contains the class DBStorage
"""
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import models
from models.base_model import BaseModel, Base
from models.quiz import Quiz
from models.option import Option
from models.question import Question
from models.flashcard import Flashcard
from models.category import Category
from models.user import User
from models.quiz_attempt import QuizAttempt
from models.quiz_response import QuizResponse

##########################################################################################

classes = {"BaseModel": BaseModel, "User": User, "Question": Question,
        "Quiz": Quiz, "Option": Option, "Flashcard": Flashcard, "Category": Category,
        "QuizAttempt": QuizAttempt, "QuizResponse": QuizResponse}



class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        FLASH_QUIZ_MYSQL_USER = getenv('FLASH_QUIZ_MYSQL_USER')
        FLASH_QUIZ_MYSQL_PWD = getenv('FLASH_QUIZ_MYSQL_PWD')
        FLASH_QUIZ_MYSQL_HOST = getenv('FLASH_QUIZ_MYSQL_HOST')
        FLASH_QUIZ_MYSQL_DB = getenv('FLASH_QUIZ_MYSQL_DB')
        ############################################################################################################
        FLASH_QUIZ_MYSQL_USER='flash_quiz_dev'
        FLASH_QUIZ_MYSQL_PWD='flash_quiz_dev_pwd'
        FLASH_QUIZ_MYSQL_HOST='localhost'
        FLASH_QUIZ_MYSQL_DB='flash_quiz_dev_db'
        # FLASH_QUIZ_TYPE_STORAGE='db'
        # FLASH_QUIZ_API_HOST='localhost'
        ############################################################################################################
        FLASH_QUIZ_ENV = 'dev'
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                    format(FLASH_QUIZ_MYSQL_USER,
                                            FLASH_QUIZ_MYSQL_PWD,
                                            FLASH_QUIZ_MYSQL_HOST,
                                            FLASH_QUIZ_MYSQL_DB))
        if FLASH_QUIZ_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        try:
            self.__session.commit()
        except:
            self.__session.rollback()
            raise

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
        Base.query = self.__session.query_property()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count


    def get_attribute(self, cls, attributes, values, select_columns=None):
        if (select_columns is None):
            queryElement = classes[cls]
        else:
            queryElement = eval(cls + "." + select_columns)
            # print(queryElement)
        
        for attr_index, attr in enumerate(attributes):
            var = eval(cls + "." + attr)
            if (attr_index == 0):
                result = self.__session.query(queryElement).filter(var == values[attr_index])
                # print(result)
            else:
                # var = eval(cls + "." + attr)
                result = result.filter(var == values[attr_index])
        result = result.all()
        # print(result)
        return result


    def search(self, cls, searchAttributes, searchValues, limit=None, order_by=None, order=None):
        theClass = classes[cls]
        for attr_index, attr in enumerate(searchAttributes):
            var = eval(cls + "." + attr)
            if (attr_index == 0):
                result = self.__session.query(theClass).filter(var.like("%" + searchValues[attr_index] + "%"))
            else:
                result = result.filter(var == searchValues[attr_index])
        if (limit is not None):
            result = result.limit(limit)
        result = result.all()
        return result

    def paginate(self, cls, page, per_page):
        theClass = classes[cls]
        # result = self.__session.query(theClass).paginate(page,per_page,error_out=False)
        result = self.__session.query(theClass).limit(per_page).offset((page - 1) * per_page)
        # print(result)
        result = result.all()
        return result
