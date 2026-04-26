from flask import Blueprint, render_template, session, redirect, url_for
from models.user import get_developer_by_user_id
from models.project import get_projects_by_owner
from models.request import get_requests_by_developer, get_pending_requests_by_owner
from models.rating import get_average_rating
from models.match import (
    get_active_match_counts_for_projects,
    get_active_matches_by_developer,
)

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    developer = get_developer_by_user_id(user_id)
    developer_id = developer['developer_id']

    all_my_projects = get_projects_by_owner(developer_id)
    
    my_projects = [p for p in all_my_projects if p['status'] == 'open'][:12]

    project_ids = [p['project_id'] for p in my_projects]
    active_counts = get_active_match_counts_for_projects(project_ids)
    for p in my_projects:
        active_count = active_counts.get(p['project_id'], 0)
        p['remaining_slots'] = max(0, p['slots_needed'] - active_count)

    incoming_requests = get_pending_requests_by_owner(developer_id, limit=10)

    sent_requests = get_requests_by_developer(
        developer_id, statuses=['pending', 'rejected']
    )[:12]

    active_matches = get_active_matches_by_developer(developer_id, limit=8)
    avg_rating = get_average_rating(developer_id)

    return render_template('dashboard/dashboard.html',
                           developer=developer,
                           my_projects=my_projects,
                           incoming_requests=incoming_requests,
                           sent_requests=sent_requests,
                           active_matches=active_matches,
                           avg_rating=avg_rating)

@bp.route('/rules')
def rules():

    return render_template('rules.html')