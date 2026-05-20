from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.admin import (
    get_global_stats, 
    get_all_projects_oversight, 
    get_all_ratings_oversight,
    get_all_developers_oversight,
    toggle_user_status_admin,
    delete_rating_admin as delete_rating_db, 
    delete_project_admin as delete_project_db
)

bp = Blueprint('admin', __name__)

def admin_required():
    return session.get('role', '').lower() == 'admin'

@bp.route('/admin')
def panel():
    if not admin_required():
        flash("Unauthorized access.", "error")
        return redirect(url_for('auth.login'))

    tab = request.args.get('tab', 'dashboard')
    show_all = request.args.get('all', '0') == '1'
    row_limit = None if show_all else 100

    context = {'tab': tab, 'show_all': show_all}

    if tab == 'dashboard':
        context['stats'] = get_global_stats()
        return render_template('admin/dashboard.html', **context)
    elif tab == 'projects':
        p_search = request.args.get('project_q', '').strip()
        context['projects'] = get_all_projects_oversight(search_term=p_search, limit=row_limit)
        context['project_q'] = p_search
        return render_template('admin/projects.html', **context)
    elif tab == 'ratings':
        r_search = request.args.get('review_q', '').strip()
        context['ratings'] = get_all_ratings_oversight(search_term=r_search, limit=row_limit)
        context['review_q'] = r_search
        return render_template('admin/ratings.html', **context)
    elif tab == 'developers':
        d_search = request.args.get('dev_q', '').strip()
        context['developers'] = get_all_developers_oversight(search_term=d_search, limit=row_limit)
        context['dev_q'] = d_search
        return render_template('admin/developers.html', **context)
    else:
        return redirect(url_for('admin.panel', tab='dashboard'))

@bp.route('/admin/delete_project/<int:project_id>', methods=['POST'])
def delete_project_admin(project_id):
    if not admin_required(): return redirect(url_for('auth.login'))
    delete_project_db(project_id)
    flash("Project deleted.", "success")
    return redirect(url_for('admin.panel', tab='projects'))

@bp.route('/admin/delete_rating/<int:rating_id>', methods=['POST'])
def delete_rating_admin(rating_id):
    if not admin_required(): return redirect(url_for('auth.login'))
    delete_rating_db(rating_id)
    flash("Rating deleted.", "success")
    return redirect(url_for('admin.panel', tab='ratings'))

@bp.route('/admin/toggle_user/<int:user_id>', methods=['POST'])
def toggle_user(user_id):
    if not admin_required(): return redirect(url_for('auth.login'))
    toggle_user_status_admin(user_id)
    flash("User access status updated.", "success")
    return redirect(url_for('admin.panel', tab='developers'))