from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user
from .models import User
from . import db, login_manager

auth_routes = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')  # Render the login template

@auth_routes.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('main.home'))

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('auth.login'))
    return render_template('register.html')  # Render the register template