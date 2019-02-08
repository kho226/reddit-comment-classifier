from app.main import bp
from flask import render_template

@bp.route('/')
@bp.route('/index')
def index():
    user = {"username": "Kyle"}
    return render_template("index.html",  title="Reddit Trends", user=user)