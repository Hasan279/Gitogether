from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.match import get_active_matches_by_developer, get_completed_matches_by_developer, get_match_by_id, complete_match
from models.project import get_project_by_id, update_project_status
from models.user import get_developer_id
from models.rating import check_existing_rating

bp = Blueprint('matches', __name__)


@bp.route('/matches')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    developer_id = get_developer_id(session['user_id'])
    active_matches = get_active_matches_by_developer(developer_id)
    session['developer_id'] = developer_id
    completed_matches = get_completed_matches_by_developer(developer_id)
    
    # check if already rated for each completed match
    for match in completed_matches:
        match['already_rated'] = bool(check_existing_rating(match['match_id'], developer_id))
        
    return render_template('matches/matches.html',
                           active_matches=active_matches,
                           completed_matches=completed_matches)


@bp.route('/matches/complete/<int:match_id>', methods=['POST'])
def complete(match_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    match = get_match_by_id(match_id)
    project = get_project_by_id(match['project_id'])
    user_dev_id = get_developer_id(session['user_id'])

    # Only the project owner can close the project
    if project['owner_id'] != user_dev_id:
        flash("You are not authorized to complete this project", "error")
        return redirect(url_for('dashboard.index'))

    complete_match(match_id)
    update_project_status(project['project_id'], 'completed')

    rated_id = match['developer_id']

    return render_template('ratings/rate.html', 
                           match=match, 
                           rated_id=rated_id)