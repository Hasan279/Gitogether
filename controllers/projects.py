from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.project import *
from models.skill import *
from models.user import *
from models.request import *

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
    project = get_project_by_id(project_id) 
    raw_skills = get_project_skills(project_id) 
    
    # group by category
    grouped_skills = {}
    for skill in raw_skills:
        cat = skill['category'] if skill.get('category') else 'Other'
        if cat not in grouped_skills:
            grouped_skills[cat] = []
        grouped_skills[cat].append(skill)
        
    return render_template('projects/detail.html', 
                           project=project, 
                           grouped_skills=grouped_skills)


@bp.route('/projects/create', methods=['GET', 'POST'])
def create():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    all_skills = get_all_skills()
    
    grouped_skills = {}
    for skill in all_skills:
        cat = skill['category'] if skill.get('category') else 'Other'
        if cat not in grouped_skills:
            grouped_skills[cat] = []
        grouped_skills[cat].append(skill)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        slots_needed = request.form.get('slots_needed', 1)
        selected_skills = request.form.getlist('skills')

        # Basic Validation
        if not title or not description:
            flash("Title and Description are required.", "error")
            return render_template('projects/create.html', grouped_skills=grouped_skills)

        try:
            slots = int(slots_needed)
            if slots < 1:
                raise ValueError
        except ValueError:
            flash("Slots must be a valid number (at least 1).", "error")
            return render_template('projects/create.html', grouped_skills=grouped_skills)

        developer_id = get_developer_id(session['user_id'])
        project_id = create_project(developer_id, title, description, location, slots)

        for skill_id in selected_skills:
            add_project_skill(project_id, skill_id, is_required=True)

        flash("Project created successfully!", "success")
        return redirect(url_for('dashboard.index'))

    return render_template('projects/create.html', grouped_skills=grouped_skills)


@bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
def edit(project_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    project = get_project_by_id(project_id)
    
    #only the owner can edit
    current_user_id = session.get('developer_id') or session.get('user_id')
    if not project or current_user_id != project['owner_id']:
        flash("Unauthorized access.", "error")
        return redirect(url_for('projects.browse'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        slots_needed = request.form.get('slots_needed', 1)
        selected_skills = request.form.getlist('skills') 

        if not title or not description:
            flash("Title and Description are required.", "error")
        else:
            update_project(project_id, title, description, location, slots_needed)

            project_skills = get_project_skills(project_id)
            for s in project_skills:
                remove_project_skill(project_id, s['skill_id'])
            
            for skill_id in selected_skills:
                add_project_skill(project_id, skill_id, is_required=True)

            flash("Project updated successfully!", "success")
            return redirect(url_for('projects.detail', project_id=project_id))

    all_skills = get_all_skills()
    current_skills = get_project_skills(project_id)

    selected_skill_ids = [s['skill_id'] for s in current_skills]

    grouped_skills = {}
    for skill in all_skills:
        cat = skill['category'] if skill.get('category') else 'Other'
        if cat not in grouped_skills:
            grouped_skills[cat] = []
        grouped_skills[cat].append(skill)

    return render_template(
        'projects/edit.html', 
        project=project, 
        grouped_skills=grouped_skills, 
        selected_skill_ids=selected_skill_ids
    )


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