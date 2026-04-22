from flask import Blueprint, session, redirect, url_for, flash
from models.request import create_request, get_request_by_id, update_request_status, check_existing_request
from models.match import create_match, check_existing_match
from models.user import get_developer_id
from models.project import get_project_by_id

bp = Blueprint('requests', __name__)


@bp.route('/requests/send/<int:project_id>', methods=['POST'])
def send(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    developer_id = get_developer_id(session['user_id'])
    project = get_project_by_id(project_id)

    if project[1] == developer_id:
        flash("You cannot request to join your own project", "error")
        return redirect(url_for('projects.detail', project_id=project_id))

    existing = check_existing_request(developer_id, project_id)
    if existing:
        flash("You have already sent a request for this project", "error")
        return redirect(url_for('projects.detail', project_id=project_id))

    create_request(developer_id, project_id)
    flash("Request sent successfully", "success")
    return redirect(url_for('projects.detail', project_id=project_id))


@bp.route('/requests/accept/<int:request_id>', methods=['POST'])
def accept(request_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    req = get_request_by_id(request_id)
    project = get_project_by_id(req[2])
    developer_id = get_developer_id(session['user_id'])

    if project[1] != developer_id:
        flash("You are not authorized to accept this request", "error")
        return redirect(url_for('dashboard.index'))

    existing = check_existing_match(req[1], req[2])
    if existing:
        flash("A match already exists for this developer and project", "error")
        return redirect(url_for('dashboard.index'))

    update_request_status(request_id, 'accepted')
    create_match(req[1], req[2])

    flash("Request accepted, match created", "success")
    return redirect(url_for('dashboard.index'))


@bp.route('/requests/reject/<int:request_id>', methods=['POST'])
def reject(request_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    req = get_request_by_id(request_id)
    project = get_project_by_id(req[2])
    developer_id = get_developer_id(session['user_id'])

    if project[1] != developer_id:
        flash("You are not authorized to reject this request", "error")
        return redirect(url_for('dashboard.index'))

    update_request_status(request_id, 'rejected')
    flash("Request rejected", "success")
    return redirect(url_for('dashboard.index'))