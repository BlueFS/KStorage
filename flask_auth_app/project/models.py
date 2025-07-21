# This knowledge was gained from Digital Ocean on how to create a login page.
# Specifically the values in the table and how to use Python3 to execute SQLAlchemy to create .sqlite files
# Additionally ChatGPT was used because the code didnt work originally to create the DB.
#  -> It told me to use "with app.app_context():" first vs. just "db.create_all(app=create_app())"
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    # adds relationship to file
    files = db.relationship('UploadedFile', backref='user', lazy=True)
    # Note for future by digital ocean: Primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

# ChatGPT was used to help make this model
# DB that stores user values


class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
