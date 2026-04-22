from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import *

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    full_name = request.form.get('full_name', '').strip()
    bio = request.form.get('bio', '').strip()
    location = request.form.get('location', '').strip()
    years_experience = request.form.get('years_experience', 0)
    contact_link = request.form.get('contact_link', '').strip()

    if not email or '@' not in email:
        flash("Invalid email address", "error")
        return redirect(url_for('auth.register'))

    if len(password) < 6:
        flash("Password must be at least 6 characters", "error")
        return redirect(url_for('auth.register'))

    if not full_name:
        flash("Full name is required", "error")
        return redirect(url_for('auth.register'))

    existing_user = get_user_by_email(email)
    if existing_user:
        flash("Email already registered", "error")
        return redirect(url_for('auth.register'))

    user_id = create_user(email, password)
    create_developer_profile(user_id, full_name, bio, location, years_experience, contact_link)

    session['user_id'] = user_id
    session['email'] = email
    session['role'] = 'developer'
    full_name = get_developer_by_user_id(session['user_id'])['full_name']
    session['full_name'] = full_name

    flash("Welcome to Gitogether!", "success")
    return redirect(url_for('dashboard.index'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if not email or not password:
        flash("Email and password are required", "error")
        return redirect(url_for('auth.login'))

    user = get_user_by_email(email)
    if not user:
        flash("Invalid email or password", "error")
        return redirect(url_for('auth.login'))

    if not verify_password(password, user['password_hash']):
        flash("Invalid email or password", "error")
        return redirect(url_for('auth.login'))

    if not user['is_active']:
        flash("Your account has been deactivated", "error")
        return redirect(url_for('auth.login'))

    session['user_id'] = user['user_id']
    session['email'] = user['email']
    session['role'] = user['role']
    full_name = get_developer_by_user_id(session['user_id'])['full_name']
    session['full_name'] = full_name
    if user['role'] == 'admin':
        return redirect(url_for('admin.panel'))

    flash("Welcome back!", "success")
    return redirect(url_for('dashboard.index'))


@bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('auth.login'))