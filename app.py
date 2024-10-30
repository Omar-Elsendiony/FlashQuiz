#!/usr/bin/python3
""" Flask Application """
from models import storage
from models.user import User
from models.base_model import BaseModel
from models.flashcard import Flashcard
from models.category import Category
from models.quiz import Quiz
from models.question import Question
from models.option import Option
# from models.review import Review

#################### flask imports ###########################################################
# import requests
from os import environ
from flask import Flask, render_template, make_response, jsonify, redirect, request, session
from flask_cors import CORS
# from flasgger import Swagger
# from flasgger.utils import swag_from
from flask_session import Session
####################### Models imports ##################################################
from models.base_model import BaseModel

from hashlib import md5

from flask import Flask, render_template, request, redirect, url_for, flash
from models import db
from models.category import Category
from models.quiz import Quiz
from models.question import Question
from models.option import Option
from models.user import User

from flask_login import LoginManager, login_required, current_user

##########################################################################################

classes = {"BaseModel": BaseModel, "User": User}


app = Flask(__name__ , static_url_path='')

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# app.register_blueprint(app_views)
# cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
cors = CORS(app)

# Initialize Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'Mathifestation API',
    'uiversion': 3
}

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Swagger(app)
Session(app)


@app.route('/', strict_slashes=False)
@app.route('/index', strict_slashes=False)
def index():
    """ Index
    ---
    responses:
      200:
        description: Index
    """
    # print(session.get("username"))
    return render_template('index.html', error=None)




# @login_required
@app.route('/create-quiz', methods=['GET', 'POST'])
def create_quiz():
    categories = Category.query.all()
    
    if request.method == 'POST':
        title = request.form['quiz-title']
        category_id = request.form['quiz-category']
        
        quiz = Quiz(title=title, creator=current_user, category_id=category_id)
        db.session.add(quiz)
        
        for i in range(1, len(request.form) // 5 + 1):  # Assuming each question has 5 form fields
            question_text = request.form[f'question-{i}']
            question_type = request.form[f'question-type-{i}']
            
            question = Question(text=question_text, question_type=question_type, quiz=quiz)
            db.session.add(question)
            
            if question_type == 'mcq':
                for j in range(1, 5):
                    option_text = request.form[f'option-{i}-{j}']
                    is_correct = request.form[f'correct-answer-{i}'] == str(j)
                    option = Option(text=option_text, is_correct=is_correct, question=question)
                    db.session.add(option)
            elif question_type == 'true-false':
                correct_answer = request.form[f'correct-answer-{i}']
                true_option = Option(text='True', is_correct=(correct_answer == 'true'), question=question)
                false_option = Option(text='False', is_correct=(correct_answer == 'false'), question=question)
                db.session.add_all([true_option, false_option])
        
        db.session.commit()
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('view_quiz', quiz_id=quiz.id))
    
    return render_template('create_quiz.html', categories=categories)





if __name__ == "__main__":
    """ Main Function """
    host = environ.get('FLASH_QUIZ_API_HOST')
    port = environ.get('FLASH_QUIZ_API_PORT')
    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True, debug=True)
