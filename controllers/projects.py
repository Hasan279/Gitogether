from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.project import create_project, get_all_open_projects, get_project_by_id, get_projects_by_owner, update_project, update_project_status, delete_project
from models.skill import get_all_skills, get_project_skills, add_project_skill, remove_project_skill
from models.user import get_developer_id
from models.request import check_existing_request

bp = Blueprint('projects', __name__)


@bp.route('/projects')
def browse():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    skill_filter = request.args.get('skill', None)
    page = int(request.args.get('page', 1))
    projects = get_all_open_projects(skill_filter=skill_filter, page=page)
    skills = get_all_skills()

    return render_template('projects/browse.html', projects=projects, skills=skills, page=page, skill_filter=skill_filter)


@bp.route('/projects/<int:project_id>')
def detail(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    project = get_project_by_id(project_id)
    if not project:
        flash("Project not found", "error")
        return redirect(url_for('projects.browse'))

    project_skills = get_project_skills(project_id)
    developer_id = get_developer_id(session['user_id'])
    existing_request = check_existing_request(developer_id, project_id)

    return render_template('projects/detail.html', project=project, 
                           project_skills=project_skills, 
                           existing_request=existing_request,
                           developer_id=developer_id)


@bp.route('/projects/create', methods=['GET', 'POST'])
def create():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        skills = get_all_skills()
        return render_template('projects/create.html', skills=skills)

    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    location = request.form.get('location', '').strip()
    slots_needed = request.form.get('slots_needed', 1)
    selected_skills = request.form.getlist('skills')

    if not title:
        flash("Title is required", "error")
        return redirect(url_for('projects.create'))

    if not description:
        flash("Description is required", "error")
        return redirect(url_for('projects.create'))

    if int(slots_needed) < 1:
        flash("Slots must be at least 1", "error")
        return redirect(url_for('projects.create'))

    developer_id = get_developer_id(session['user_id'])
    project_id = create_project(developer_id, title, description, location, slots_needed)

    for skill_id in selected_skills:
        add_project_skill(project_id, skill_id, is_required=True)

    flash("Project created successfully", "success")
    return redirect(url_for('dashboard.index'))


@bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
def edit(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    project = get_project_by_id(project_id)
    developer_id = get_developer_id(session['user_id'])

    if project['owner_id'] != developer_id:
        flash("You are not authorized to edit this project", "error")
        return redirect(url_for('dashboard.index'))

    if request.method == 'GET':
        skills = get_all_skills()
        project_skills = get_project_skills(project_id)
        return render_template('projects/edit.html', project=project, skills=skills, project_skills=project_skills)

    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    location = request.form.get('location', '').strip()
    slots_needed = request.form.get('slots_needed', 1)
    selected_skills = request.form.getlist('skills')

    if not title:
        flash("Title is required", "error")
        return redirect(url_for('projects.edit', project_id=project_id))

    update_project(project_id, title, description, location, slots_needed)
    remove_project_skill(project_id)

    for skill_id in selected_skills:
        add_project_skill(project_id, skill_id, is_required=True)

    flash("Project updated successfully", "success")
    return redirect(url_for('dashboard.index'))


@bp.route('/projects/<int:project_id>/delete', methods=['POST'])
def delete(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    project = get_project_by_id(project_id)
    developer_id = get_developer_id(session['user_id'])

    if project['owner_id'] != developer_id:
        flash("You are not authorized to delete this project", "error")
        return redirect(url_for('dashboard.index'))

    delete_project(project_id)
    flash("Project deleted successfully", "success")
    return redirect(url_for('dashboard.index'))