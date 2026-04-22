from flask import Blueprint, render_template, session, redirect, url_for
from models.project import *
from models.user import *
from models.request import *
bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def index():
    user_id = session['user_id']
    # get developer profile
    dev = get_developer_by_user_id(user_id)
    # get projects by owner
    dev_id = get_developer_id(user_id)
    projects = get_projects_by_owner(dev_id)
    # get requests by developer
    req = get_requests_by_developer(dev_id)
    # get active matches
    # get last 3 completed matches
    # get average rating
    # render dashboard.html with all of the above
    pass