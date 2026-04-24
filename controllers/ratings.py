from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from models.rating import create_rating, check_existing_rating
from models.match import get_match_by_id
from models.user import get_developer_id

bp = Blueprint('ratings', __name__)

@bp.route('/ratings/submit/<int:match_id>', methods=['POST'])
def submit(match_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    match = get_match_by_id(match_id)
    rater_id = get_developer_id(session['user_id'])
    rated_id = request.form.get('rated_id')
    score = int(request.form.get('score'))
    review = request.form.get('review', '').strip()

    if score < 1 or score > 5:
        flash("Score must be between 1 and 5", "error")
        return redirect(request.referrer)

    existing = check_existing_rating(match_id, rater_id)
    if existing:
        flash("You have already rated this collaboration", "error")
        return redirect(url_for('dashboard.index'))

    create_rating(match_id, rater_id, rated_id, score, review)
    flash("Rating saved!", "success")
    
    if match['status'] == 'active':
        return redirect(url_for('matches.review_team', project_id=match['project_id']))
    else:
        return redirect(url_for('matches.index'))


@bp.route('/ratings/rate/<int:match_id>')
def rate(match_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    match = get_match_by_id(match_id)
    user_dev_id = get_developer_id(session['user_id'])

    if match['owner_id'] == user_dev_id:
        target_id = match['developer_id']
    else:
        target_id = match['owner_id']

    return render_template('ratings/rate.html', match=match, rated_id=target_id)