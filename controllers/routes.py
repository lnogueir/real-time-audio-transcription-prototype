from flask import Blueprint, render_template, request, jsonify

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')
