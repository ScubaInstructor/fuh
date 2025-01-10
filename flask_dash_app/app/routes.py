from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from . import db

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
@login_required
def home():
    return render_template('home.html')

@main_routes.route('/dashboard')
@login_required
def dashboard():
    print(f"User authenticated: {current_user.is_authenticated}")  # Debugging
    #return render_template('dashboard.html', username=current_user.username)
    return redirect('/dashboard/')