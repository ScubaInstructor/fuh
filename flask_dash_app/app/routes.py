from flask import Blueprint, jsonify, render_template, redirect, request
from flask_login import login_required, current_user
import jwt
from . import db, app, MODELNAME, MODELPATH, compute_file_hash, model_hash

main_routes = Blueprint('main', __name__)
model_hash = compute_file_hash(MODELPATH + MODELNAME)

@main_routes.route('/')
@login_required
def home():
    return render_template('home.html')

@main_routes.route('/inbox')
@login_required
def dashboard():
    print(f"User authenticated: {current_user.is_authenticated}")  # Debugging
    #return render_template('dashboard.html', username=current_user.username)
    return redirect('/inbox/')


@main_routes.route('/get_model_hash', methods=['GET'])
def get_model_hash():
    # check auth
    token = request.headers.get('Authorization').split()[1]
    try:
        payload = jwt.decode(token, app.secret_key, options={"verify_exp": False} , algorithms=['HS256'])
    except jwt.ExpiredSignatureError: # Not in use TODO check if neccessary
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    # Everything is well and we return the hash
    # TODO insert hash and add the respective functions and variables
    return jsonify({'message': 'Access granted', 'model_hash': model_hash})
