from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.user import *
from models.skill import *
from models.rating import get_average_rating, get_ratings_by_developer

bp = Blueprint('developers', __name__)

@bp.route('/developers')
def browse():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    skill_filter = request.args.get('skill', '')
    search_query = request.args.get('q', '').strip() # New: Name search
    page = request.args.get('page', 1, type=int)
    
    skills = get_all_skills()

    if search_query:
        developers = get_developer_by_name(search_query)
    else:
        developers = get_all_developers(
            skill_filter=skill_filter if skill_filter else None, 
            page=page
        )

    return render_template('developers/browse.html', 
                           developers=developers, 
                           skills=skills, 
                           page=page, 
                           skill_filter=skill_filter,
                           search_query=search_query) 

@bp.route('/developers/<int:developer_id>')
def profile(developer_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    developer_data = get_developer_by_id(developer_id)
    
    if not developer_data:
        flash("Developer not found", "error")
        return redirect(url_for('developers.browse'))

    skills = get_developer_skills(developer_id)
    avg_rating = get_average_rating(developer_id)
    reviews = get_ratings_by_developer(developer_id)

    return render_template('developers/profile.html',
                           developer=developer_data,
                           developer_skills=skills,
                           avg_rating=avg_rating,
                           reviews=reviews)
    
@bp.route('/developers/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    u_id = session['user_id']

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        bio = request.form.get('bio')
        location = request.form.get('location')
        years_exp = request.form.get('years_experience')
        link = request.form.get('contact_link')
        
        update_developer_profile(u_id, full_name, bio, location, years_exp, link)
        flash("Profile updated!", "success")
        return redirect(url_for('developers.edit_profile'))

    dev = get_developer_by_user_id(u_id)
    skills = get_all_skills()
    dev_skills = get_developer_skills(dev['developer_id'])
    
    return render_template('developers/edit_profile.html', 
                           developer=dev, 
                           all_skills=skills, 
                           dev_skills=dev_skills)
@bp.route('/developers/skills/add', methods=['POST'])
def add_skill():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    developer_id = get_developer_id(session['user_id'])
    skill_id = request.form.get('skill_id')
    proficiency = request.form.get('proficiency_level')
    if skill_id and proficiency:
        add_developer_skill(developer_id, skill_id, proficiency)
    return redirect(url_for('developers.edit_profile'))

@bp.route('/developers/skills/remove/<int:skill_id>', methods=['POST'])
def remove_skill(skill_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    developer_id = get_developer_id(session['user_id'])
    remove_developer_skill(developer_id, skill_id)
    return redirect(url_for('developers.edit_profile'))