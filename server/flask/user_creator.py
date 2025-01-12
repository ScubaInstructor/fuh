import sys
import os
import base64
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from akins_verbesserter_flask_server import User, SQLITE_PATH, db, app

# Flask application and database configuration
#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_PATH
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

# # User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)
#     salt = db.Column(db.String(150), nullable=False)  # Salt for the password

# Function to validate user input
def validate_input(username, password):
    username_regex = r'^[A-Za-z0-9_]{3,20}$'  # Alphanumeric, 3-20 characters
    password_regex = r'^.{8,}$'  # At least 8 characters

    if not re.match(username_regex, username):
        raise ValueError("Username must contain 3-20 alphanumeric characters or underscores.")
    
    if not re.match(password_regex, password):
        raise ValueError("Password must be at least 8 characters long.")

# Function to create the database and add a user
def create_user(username, password):
    # Check if the database exists and create tables if not
    with app.app_context():
        db.create_all()  # Creates the database and tables if they do not exist
        
        # Validate user input
        try:
            validate_input(username, password)
        except ValueError as e:
            print(e)
            return
        
        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"User '{username}' already exists.")
            return  

        # Generate a salt
        salt = base64.b64encode(os.urandom(16)).decode('utf-8')

        # Hash the password with the salt
        hashed_password = generate_password_hash(password + salt)

        # Create a new user
        new_user = User(username=username, password=hashed_password, salt=salt)
        db.session.add(new_user)
        db.session.commit()
        print(f"User  '{username}' has been successfully created.")

# Main part of the program
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <username> <password>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    create_user(username, password)