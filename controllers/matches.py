from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.match import (
    get_active_matches_by_developer, 
    get_completed_matches_by_developer, 
    get_match_by_id, 
    get_unrated_team_members, 
    complete_project_matches
)
from models.project import get_project_by_id
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
    
    for match in completed_matches:
        match['already_rated'] = bool(check_existing_rating(match['match_id'], developer_id))
        
    return render_template('matches/matches.html',
                           active_matches=active_matches,
                           completed_matches=completed_matches)


@bp.route('/projects/<int:project_id>/review_team', methods=['GET'])
def review_team(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    rater_id = get_developer_id(session['user_id'])
    project = get_project_by_id(project_id)
    
    if project['owner_id'] != rater_id:
        flash("You are not authorized to complete this project.", "error")
        return redirect(url_for('dashboard.index'))
    
    next_dev_to_rate = get_unrated_team_members(project_id, rater_id)
    
    if next_dev_to_rate:
        mock_match = {
            'match_id': next_dev_to_rate['match_id'],
            'project_id': project_id,
            'title': project['title']
        }
        
        return render_template('ratings/rate.html', 
                               match=mock_match, 
                               rated_id=next_dev_to_rate['developer_id'],
                               developer_name=next_dev_to_rate['full_name'])
    else:
        complete_project_matches(project_id) 
        flash("Project completed and all team members rated!", "success")
        return redirect(url_for('dashboard.index'))