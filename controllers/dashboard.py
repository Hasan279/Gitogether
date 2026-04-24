from flask import Blueprint, render_template, session, redirect, url_for
from models.user import get_developer_by_user_id, get_developer_id
from models.project import get_projects_by_owner
from models.request import get_requests_by_developer, get_requests_by_project
from models.match import get_active_matches_by_developer, get_completed_matches_by_developer
from models.rating import get_average_rating

bp = Blueprint('dashboard', __name__)


@bp.route('/dashboard')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    developer = get_developer_by_user_id(user_id)
    developer_id = developer['developer_id']

    all_my_projects = get_projects_by_owner(developer_id)
    my_projects = [p for p in all_my_projects if p['status'] == 'active']

    all_incoming = []
    for project in all_my_projects:
        reqs = get_requests_by_project(project['project_id'])
        all_incoming.extend(reqs)
    
    incoming_requests = [r for r in all_incoming if r['status'] == 'pending']

    all_sent = get_requests_by_developer(developer_id)
    sent_requests = [r for r in all_sent if r['status'] in ['pending', 'rejected']]

    active_matches = get_active_matches_by_developer(developer_id)
    completed_matches = get_completed_matches_by_developer(developer_id, limit=3)
    avg_rating = get_average_rating(developer_id)

    return render_template('dashboard/dashboard.html',
                           developer=developer,
                           my_projects=my_projects,
                           incoming_requests=incoming_requests,
                           sent_requests=sent_requests,
                           active_matches=active_matches,
                           completed_matches=completed_matches,
                           avg_rating=avg_rating)

@bp.route('/rules')
def rules():

    return render_template('rules.html')