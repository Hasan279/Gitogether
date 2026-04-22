from flask import Blueprint, render_template, request, session

bp = Blueprint('developers', __name__)

@bp.route('/developers')
def browse():
    # get skill filter from query params
    # get page number from query params
    # get all developers filtered and paginated
    # render developers/browse.html
    pass

@bp.route('/developers/<int:developer_id>')
def profile(developer_id):
    # get developer profile
    # get developer skills
    # get average rating
    # get ratings/reviews
    # render developers/profile.html
    pass