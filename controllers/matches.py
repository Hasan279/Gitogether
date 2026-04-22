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
    completed_matches = get_completed_matches_by_developer(developer_id)

    return render_template('matches/matches.html',
                           active_matches=active_matches,
                           completed_matches=completed_matches)


@bp.route('/matches/complete/<int:match_id>', methods=['POST'])
def complete(match_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    match = get_match_by_id(match_id)
    project = get_project_by_id(match[2])
    developer_id = get_developer_id(session['user_id'])

    if project[1] != developer_id:
        flash("Only the project owner can mark a project as completed", "error")
        return redirect(url_for('matches.index'))

    complete_match(match_id)
    update_project_status(project[0], 'completed')

    flash("Project marked as completed", "success")
    return redirect(url_for('matches.index'))