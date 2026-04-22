from flask import Blueprint, render_template, session, redirect, url_for

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def index():
    # get session user_id
    # get developer profile
    # get projects by owner
    # get requests by developer
    # get active matches
    # get last 3 completed matches
    # get average rating
    # render dashboard.html with all of the above
    pass