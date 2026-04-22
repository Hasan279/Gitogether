from flask import Blueprint, request, session, redirect, url_for

bp = Blueprint('ratings', __name__)

@bp.route('/ratings/submit/<int:match_id>', methods=['POST'])
def submit(match_id):
    # get match by id
    # check match status is completed
    # check no existing rating from this user for this match
    # get score and review from form
    # validate score is between 1 and 5
    # create rating
    # redirect to matches page
    pass