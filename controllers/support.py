from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.support import create_query
from models.user import get_developer_id

bp = Blueprint('support', __name__)

@bp.route('/support', methods=['GET', 'POST'])
def contact():
    if 'user_id' not in session:
        flash("You must be logged in to contact support.", "error")
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        dev_id = get_developer_id(session['user_id'])
        if not dev_id:
            flash("You need to complete your profile before contacting support.", "error")
            return redirect(url_for('dashboard.index'))
            
        if not subject or not message:
            flash("Subject and message are required.", "error")
        else:
            create_query(dev_id, subject, message)
            flash("Your message has been sent to the admin team.", "success")
            return redirect(url_for('dashboard.index'))
            
    return render_template('support/contact.html')
