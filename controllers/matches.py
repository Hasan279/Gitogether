from flask import Blueprint, render_template, session, redirect, url_for

bp = Blueprint('matches', __name__)

@bp.route('/matches')
def index():
    # get developer_id from session
    # get active matches
    # get completed matches
    # render matches/matches.html
    pass

@bp.route('/matches/complete/<int:match_id>', methods=['POST'])
def complete(match_id):
    # get match by id
    # check current user is the project owner
    # complete match
    # update project status to completed
    # redirect to dashboard
    pass