# Some of this was gained from Digital Ocean on how to create a login page.
# Specifically how to use Blueprint and the utilization of different routes for GET and POST
# using this new format which includes going into the main and auth files to retrieve routes
from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
# ChatGPT was used to help make the UploadedFile model
from .models import User, UploadedFile
from . import db
import os

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    # Check is user exists and if password matches
    user = User.query.filter_by(email=email).first()
    # If not, render an error and reload page
    if not user or not check_password_hash(user.password, password):
        flash('Invalid username or password. Please try again')
        return redirect(url_for('auth.login'))

    # Else log in
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # Gets data from form
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    # Checks if user already exists
    user = User.query.filter_by(email=email).first()
    # User is found
    if user:
        flash('Account already made with this email!')
        return redirect(url_for('auth.signup'))
    if confirm_password != password:
        flash('Password does not match confirmation!')
        return redirect(url_for('auth.signup'))
    # Generates new user data
    new_user = User(email=email, name=name, password=generate_password_hash(
        password, method='pbkdf2:sha256'))
    # Adds user
    db.session.add(new_user)
    db.session.commit()
    # Redirct to login
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/email_change', methods=['POST'])
@login_required
def email_change():
    email_current = request.form.get("email_current")
    email_new = request.form.get("email_new")
    email_confirm = request.form.get("email_new")
    user_email = current_user.email
    # Checks if current email is same as actual
    if email_current != user_email:
        flash('Email not correct! Please try again', 'email')
        return redirect(url_for('main.settings'))
    # Checks if email is same as current
    if email_new == user_email:
        flash('New email cannot be same as current email!', 'email')
        return redirect(url_for('main.settings'))
    # Checks confirmation email
    if email_new != email_confirm:
        flash('New email does not match confirmation!', 'email')
        return redirect(url_for('main.settings'))

    # Changes the email
    current_user.email = email_new
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/password_change', methods=['POST'])
@login_required
def password_change():
    password_current = request.form.get("password_current")
    password_new = request.form.get("password_new")
    password_confirm = request.form.get("password_confirm")
    user_password = current_user.password
    # Checks if current password matches
    if not check_password_hash(user_password, password_current):
        flash('Password not correct! Please try again', 'password')
        return redirect(url_for('main.settings'))
    # Checks if new password is same as current password
    if password_new == password_current:
        flash('New password cannot be same as current password!', 'password')
        return redirect(url_for('main.settings'))
    # Confirms two passwords are the same
    if password_new != password_confirm:
        flash('New password does not match confirmation!', 'password')
        return redirect(url_for('main.settings'))

    # Changes the password
    current_user.password = generate_password_hash(password_new, method='pbkdf2:sha256')
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/name_change', methods=['POST'])
@login_required
def name_change():
    new_name = request.form.get("new_name")
    # Check if new name is same as current name
    if new_name == current_user.name:
        flash('New name cannot be same as current name', 'name')
        return redirect(url_for('main.settings'))

    # Changes the name
    current_user.name = new_name
    db.session.commit()
    return redirect(url_for('main.profile'))


# Backend to upload file -- ChatGPT was used to store this in the DB correctly
UPLOAD_FOLDER = 'static/uploads'


@auth.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'resume' not in request.files:
        flash('No file part', 'empty')
        return redirect(url_for('main.profile'))

    file = request.files['resume']
    if file.filename == '':
        flash('No file selected!', 'empty')
        return redirect(url_for('main.profile'))

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        # Ensure the directory exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Saves the actual file
        file.save(filepath)

        # Saves it to the DB
        new_file = UploadedFile(
            filename=filename,
            filepath=filepath,
            user_id=current_user.id,
            date_uploaded=datetime.now(timezone.utc)
        )
        db.session.add(new_file)
        db.session.commit()

        flash('File uploaded successfully!', 'success')
    else:
        flash('File upload failed!', 'failed')

    return redirect(url_for('main.profile'))
