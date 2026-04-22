from flask import Blueprint, request, session, redirect, url_for, flash
from models.rating import create_rating, check_existing_rating
from models.match import get_match_by_id
from models.user import get_developer_id

bp = Blueprint('ratings', __name__)


@bp.route('/ratings/submit/<int:match_id>', methods=['POST'])
def submit(match_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    match = get_match_by_id(match_id)

    if match['status'] != 'completed':
        flash("You can only rate completed collaborations", "error")
        return redirect(url_for('matches.index'))

    rater_id = get_developer_id(session['user_id'])
    rated_id = request.form.get('rated_id')
    score = int(request.form.get('score'))
    review = request.form.get('review', '').strip()

    if score < 1 or score > 5:
        flash("Score must be between 1 and 5", "error")
        return redirect(url_for('matches.index'))

    existing = check_existing_rating(match_id, rater_id)
    if existing:
        flash("You have already rated this collaboration", "error")
        return redirect(url_for('matches.index'))

    create_rating(match_id, rater_id, rated_id, score, review)
    flash("Rating submitted successfully", "success")
    return redirect(url_for('matches.index'))