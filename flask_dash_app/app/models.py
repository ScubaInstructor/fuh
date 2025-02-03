import base64
import os
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(150), nullable=False)  # Salt for the password
    role = db.Column(db.String(20), default='user', nullable=False)  # Role of User

    def set_password(self, password):
        self.salt =  base64.b64encode(os.urandom(150)).decode('utf-8')
        self.password_hash = generate_password_hash(password + self.salt)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + self.salt)
    
    def is_admin(self):
        return self.role == 'admin'