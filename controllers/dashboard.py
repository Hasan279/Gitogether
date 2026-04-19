from flask import Blueprint, render_template, session

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def index():
    return render_template('dashboard/dashboard.html')