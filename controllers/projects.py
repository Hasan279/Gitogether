from flask import Blueprint, render_template, request, session, redirect, url_for

bp = Blueprint('projects', __name__)

@bp.route('/projects')
def browse():
    # get skill filter from query params
    # get page number from query params
    # get all open projects filtered and paginated
    # render projects/browse.html
    pass

@bp.route('/projects/<int:project_id>')
def detail(project_id):
    # get project by id
    # get project skills
    # check if current user already sent a request
    # render projects/detail.html
    pass

@bp.route('/projects/create', methods=['GET', 'POST'])
def create():
    # GET: get all skills, render projects/create.html
    # POST: validate input, create project, add project skills, redirect to dashboard
    pass

@bp.route('/projects/<int:project_id>/delete', methods=['POST'])
def delete(project_id):
    # check current user is the owner
    # delete project
    # redirect to dashboard
    pass