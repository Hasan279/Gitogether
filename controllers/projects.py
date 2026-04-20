from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# TODO: Import your functions from models.projects here
# from models.projects import get_all_open_projects, create_project, ...

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/', methods=['GET'])
def list_projects():
    # TODO: Get 'skill' from request.args
    # TODO: Call get_all_open_projects()
    # TODO: Return render_template('projects/list.html', projects=projects)
    pass


@projects_bp.route('/<int:project_id>', methods=['GET'])
def view_project(project_id):
    # TODO: Call get_project_by_id(project_id)
    # TODO: Handle 404 if project doesn't exist
    # TODO: Return render_template('projects/view.html', project=project)
    pass


@projects_bp.route('/create', methods=['GET', 'POST'])
def new_project():
    # Security Check
    if 'user_id' not in session:
        flash("You must be logged in to post a project.", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # TODO: Extract title, description, location, slots_needed from request.form
        # TODO: Call create_project(...)
        # TODO: Flash success message
        # TODO: Redirect to the new project's view page
        pass

    # GET request: show the blank form
    # TODO: Return render_template('projects/create.html')
    pass


@projects_bp.route('/manage', methods=['GET'])
def manage_my_projects():
    # Security Check
    if 'user_id' not in session:
        flash("Please log in to manage your projects.", "error")
        return redirect(url_for('auth.login'))

    # TODO: Call get_projects_by_owner(session['user_id'])
    # TODO: Return render_template('projects/manage.html', projects=projects)
    pass


@projects_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    # Security Check
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # TODO: Fetch the project to verify ownership and pre-fill the form
    
    if request.method == 'POST':
        # TODO: Extract updated fields from request.form
        # TODO: Call update_project(...)
        # TODO: Redirect to manage dashboard or project view
        pass

    # GET request: show form with existing data
    # TODO: Return render_template('projects/edit.html', project=project)
    pass


@projects_bp.route('/<int:project_id>/status', methods=['POST'])
def update_status(project_id):
    # Security Check
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # TODO: Verify the logged-in user owns this project
    # TODO: Extract the new 'status' from request.form
    # TODO: Call update_project_status(...)
    # TODO: Redirect back to the manage dashboard
    pass