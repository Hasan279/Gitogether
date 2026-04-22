from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.user import get_developer_id, get_all_developers, get_developer_by_id
from models.skill import get_all_skills, get_developer_skills
from models.rating import get_average_rating, get_ratings_by_developer

bp = Blueprint('developers', __name__)


@bp.route('/developers')
def browse():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    skill_filter = request.args.get('skill', None)
    page = int(request.args.get('page', 1))
    developers = get_all_developers(skill_filter=skill_filter, page=page)
    skills = get_all_skills()

    return render_template('developers/browse.html', developers=developers, skills=skills, page=page, skill_filter=skill_filter)


@bp.route('/developers/<int:developer_id>')
def profile(developer_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    developer = get_developer_by_id(developer_id)
    if not developer:
        flash("Developer not found", "error")
        return redirect(url_for('developers.browse'))

    developer_skills = get_developer_skills(developer_id)
    avg_rating = get_average_rating(developer_id)
    reviews = get_ratings_by_developer(developer_id)

    return render_template('developers/profile.html',
                           developer=developer,
                           developer_skills=developer_skills,
                           avg_rating=avg_rating,
                           reviews=reviews)