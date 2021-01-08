from flask import Blueprint, render_template, request, session

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/video')
def video():
    return render_template('video.html')

@routes.route('/charts')
def charts():
    return render_template('charts.html')
