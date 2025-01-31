from flask import session, Blueprint, request, redirect, url_for, flash, render_template
from flask_login import UserMixin, login_user, logout_user
from .models import User
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

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
            session['username'] = username
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')  # Render the login template

@auth_routes.route('/logout')
def logout():
    session.pop('username', None)
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('main.home'))

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_role = request.form.get('role', 'user')   # e.g., from a dropdown
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
        else:
            new_user = User(username=username, role=user_role)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('auth.login'))
    return render_template('register.html', roles=['admin','user'])  # Render the register template