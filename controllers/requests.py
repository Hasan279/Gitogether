from flask import Blueprint, request, session, redirect, url_for

bp = Blueprint('requests', __name__)

@bp.route('/requests/send/<int:project_id>', methods=['POST'])
def send(project_id):
    # get developer_id from session
    # check existing request to prevent duplicates
    # create request
    # redirect to projects detail page
    pass

@bp.route('/requests/accept/<int:request_id>', methods=['POST'])
def accept(request_id):
    # get request by id
    # check current user is the project owner
    # update request status to accepted
    # create match
    # redirect to dashboard
    pass

@bp.route('/requests/reject/<int:request_id>', methods=['POST'])
def reject(request_id):
    # get request by id
    # check current user is the project owner
    # update request status to rejected
    # redirect to dashboard
    pass