from flask import Blueprint, session, redirect, url_for, flash
from models.request import create_request, get_request_by_id, update_request_status, check_pending_request
from models.match import *
from models.user import get_developer_id
from models.project import *

bp = Blueprint('requests', __name__)


@bp.route('/requests/send/<int:project_id>', methods=['POST'])
def send(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    developer_id = get_developer_id(session['user_id'])
    project = get_project_by_id(project_id)

    if project['owner_id'] == developer_id:
        flash("You cannot request to join your own project", "error")
        return redirect(url_for('projects.detail', project_id=project_id))

    existing = check_pending_request(developer_id, project_id)
    if existing:
        flash("You have already sent a request for this project", "error")
        return redirect(url_for('projects.detail', project_id=project_id))

    # We do NOT check slots here. Anyone can apply!
    create_request(developer_id, project_id)
    flash("Request sent successfully", "success")
    return redirect(url_for('projects.detail', project_id=project_id))


@bp.route('/requests/accept/<int:request_id>', methods=['POST'])
def accept(request_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    req = get_request_by_id(request_id)
    project = get_project_by_id(req['project_id'])
    developer_id = get_developer_id(session['user_id'])
  
    if int(project['owner_id']) != int(developer_id):
        flash("You are not authorized to accept this request", "error")
        return redirect(url_for('dashboard.index'))

    existing = check_existing_match(req['developer_id'], req['project_id'])
    if existing:
        flash("A match already exists for this developer and project", "error")
        return redirect(url_for('dashboard.index'))

    current_members = get_active_match_count(req['project_id'])
    if current_members >= project['slots_needed']:
        flash("Cannot accept. This project has already reached its member limit!", "error")
        return redirect(url_for('dashboard.index'))

    update_request_status(request_id, 'accepted')

    new_member_count = current_members + 1
    
    if new_member_count >= project['slots_needed']:
        update_project_status(req['project_id'], 'active')
        flash("Request accepted! Your team is now full. Project hidden from marketplace.", "success")
    else:
        remaining = project['slots_needed'] - new_member_count
        flash(f"Request accepted! {remaining} slot(s) remaining.", "success")

    return redirect(url_for('dashboard.index'))


@bp.route('/requests/reject/<int:request_id>', methods=['POST'])
def reject(request_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    req = get_request_by_id(request_id)
    project = get_project_by_id(req['project_id'])
    developer_id = get_developer_id(session['user_id'])

    if int(project['owner_id']) != int(developer_id):
        flash("You are not authorized to reject this request", "error")
        return redirect(url_for('dashboard.index'))

    update_request_status(request_id, 'rejected')
    flash("Request rejected", "success")
    return redirect(url_for('dashboard.index'))