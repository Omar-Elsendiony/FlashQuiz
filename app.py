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

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
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
        db.new(quiz)
        
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


@app.route('/view_quiz/<int:quiz_id>', methods=['GET'])
def view_quiz():
    return render_template('create_quiz.html')

@app.route('/view_quizzes', methods=['GET'])
def view_quizzes():
    quizzes = Quiz.query.all()
    return render_template('view_quizzes.html', quizzes=quizzes)


@app.route('/view_flashcards', methods=['GET'])
def view_flashcards():
    flashcards = Flashcard.query.all()
    return render_template('view_flashcards.html', flashcards=flashcards)

@app.route('/create-flashcard', methods=['GET', 'POST'])
def create_flashcard():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        
        flashcard = Flashcard(question=question, answer=answer, creator=current_user)
        db.session.add(flashcard)
        db.session.commit()
        flash('Flashcard created successfully!', 'success')
        return redirect(url_for('view_flashcards'))
    
    return render_template('create_flashcard.html')



@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Input validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('sign_up'))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('sign_up'))

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('sign_up'))

        existing_email = User.query.filter_by(email=email).first()
        print(existing_email)
        if existing_email:
            flash('Email already registered', 'error')
            return redirect(url_for('sign_up'))

        # Create new user
        new_user = User(
            username = username,
            email = email,
            password = password
        )

        try:
            db.new(new_user)
            db.save()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            # db.session.rollback()
            flash('An error occurred during registration', 'error')
            return redirect(url_for('sign_up'))

    return render_template('sign_up.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('index'))

    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))



import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import re
# Simulated database (replace with actual database in production)
password_reset_tokens = {}
def validate_email(email):
    """Basic email validation"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_password(password):
    """Basic password validation"""
    # At least 8 characters, one uppercase, one lowercase, one number
    return (len(password) >= 8 and 
            any(c.isupper() for c in password) and 
            any(c.islower() for c in password) and 
            any(c.isdigit() for c in password))
    
def generate_reset_token(email):
    """
    Generate a unique password reset token for the given email
    Token expires in 1 hour
    """
    # Generate a secure random token
    token = secrets.token_urlsafe(32)
    
    # Store token with expiration time
    password_reset_tokens[email] = {
        'token': token,
        'expires_at': datetime.now() + timedelta(hours=1)
    }
    
    return token

def send_reset_email(email, reset_token):
    """
    Send password reset email with reset link
    Note: Replace with your actual email configuration
    """
    try:
        # Email configuration (use environment variables in production)
        sender_email = "your_app_email@example.com"
        sender_password = "your_app_email_password"
        
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = "Password Reset Request"
        
        # Create reset link 
        reset_link = f"http://yourdomain.com/reset-password?token={reset_token}"
        
        # Email body
        body = f"""
        You have requested a password reset for your account.
        
        Click the link below to reset your password:
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you did not request this reset, please ignore this email.
        """
        
        message.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        return True
    except Exception as e:
        # Log the error in a real application
        print(f"Email sending failed: {e}")
        return False

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """
    Handle password reset token verification and password reset
    """
    if request.method == 'GET':
        # Verify reset token from URL
        token = request.args.get('token')
        
        # Find email associated with this token
        reset_email = None
        for email, token_info in password_reset_tokens.items():
            if token_info['token'] == token:
                # Check if token is still valid
                if token_info['expires_at'] > datetime.now():
                    reset_email = email
                    break
        
        if reset_email:
            # Render password reset form
            return render_template('reset_password.html', email=reset_email)
        else:
            flash('Invalid or expired reset token', 'error')
            return redirect(url_for('forgot_password'))
    
    elif request.method == 'POST':
        # Process password reset form submission
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate inputs
        if not new_password or not confirm_password:
            flash('Please fill in all fields', 'error')
            return render_template('reset_password.html', email=email)
        
        if new_password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('reset_password.html', email=email)
        
        if not validate_password(new_password):
            flash('Password must be at least 8 characters and include uppercase, lowercase, and number', 'error')
            return render_template('reset_password.html', email=email)
        
        # TODO: Update password in database
        # This would typically involve:
        # 1. Hash the new password
        # 2. Update user's password in database
        # 3. Clear any existing reset tokens for this email
        
        # Remove the used reset token
        if email in password_reset_tokens:
            del password_reset_tokens[email]
        
        flash('Password successfully reset', 'success')
        return redirect(url_for('login'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Validation
        if not email:
            flash('Please enter your email', 'error')
            return render_template('forgot_password.html')
        
        if not validate_email(email):
            flash('Invalid email format', 'error')
            return render_template('forgot_password.html')
        
        # TODO: In a real application, check if email exists in database
        
        # Generate reset token
        reset_token = generate_reset_token(email)
        
        # Send reset email
        if send_reset_email(email, reset_token):
            flash('Password reset instructions sent!', 'info')
            return redirect(url_for('login'))
        else:
            flash('Failed to send reset instructions. Please try again.', 'error')
            return render_template('forgot_password.html')
    
    return render_template('forgot_password.html')

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
