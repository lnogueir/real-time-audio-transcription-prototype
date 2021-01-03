from flask import Blueprint, render_template, request, jsonify, session


routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    session['username'] = 'username'
    return render_template('index.html')
@routes.route('/sessionTest')
def sessionTest():
    print(session.get('username', None)) # how you get the session second parameter return value if session not set. 
    return render_template('index.html')