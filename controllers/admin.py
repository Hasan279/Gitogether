from flask import Blueprint, render_template, session, redirect, url_for

bp = Blueprint('admin', __name__)

@bp.route('/admin')
def panel():
    # check current user role is admin
    # get all users
    # get all projects
    # render admin/panel.html
    pass

@bp.route('/admin/deactivate/<int:user_id>', methods=['POST'])
def deactivate(user_id):
    # check current user role is admin
    # deactivate user
    # redirect to admin panel
    pass

@bp.route('/admin/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    # check current user role is admin
    # delete project
    # redirect to admin panel
    pass