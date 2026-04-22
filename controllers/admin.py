from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.project import delete_project, get_all_open_projects
from models.user import deactivate_user, get_all_developers

bp = Blueprint('admin', __name__)


def admin_required():
    if 'user_id' not in session or session.get('role') != 'admin':
        return False
    return True


@bp.route('/admin')
def panel():
    if not admin_required():
        flash("Access denied", "error")
        return redirect(url_for('auth.login'))

    users = get_all_developers()
    projects = get_all_open_projects()

    return render_template('admin/panel.html', users=users, projects=projects)


@bp.route('/admin/deactivate/<int:user_id>', methods=['POST'])
def deactivate(user_id):
    if not admin_required():
        flash("Access denied", "error")
        return redirect(url_for('auth.login'))

    deactivate_user(user_id)
    flash("User deactivated successfully", "success")
    return redirect(url_for('admin.panel'))


@bp.route('/admin/delete_project/<int:project_id>', methods=['POST'])
def delete_project_admin(project_id):
    if not admin_required():
        flash("Access denied", "error")
        return redirect(url_for('auth.login'))

    delete_project(project_id)
    flash("Project deleted successfully", "success")
    return redirect(url_for('admin.panel'))