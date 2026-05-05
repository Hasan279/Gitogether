from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import *
import time
from collections import defaultdict

bp = Blueprint('auth', __name__)
FAILED_LOGINS_BY_IP = defaultdict(list)
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300

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

    if get_user_by_email(email):
        flash("Email already registered", "error")
        return redirect(url_for('auth.register'))

    user_id = create_user(email, password)
    create_developer_profile(user_id, full_name, bio, location, years_experience, contact_link)

    dev = get_developer_by_user_id(user_id)

    session['user_id'] = user_id
    session['email'] = email
    session['role'] = 'developer'
    session['full_name'] = full_name
    session['developer_id'] = dev['developer_id']

    flash("Welcome to Gitogether!", "success")
    return redirect(url_for('dashboard.index'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr or '')
    if ',' in client_ip:
        client_ip = client_ip.split(',')[0].strip()
    now = time.time()
    attempts = [
        ts for ts in FAILED_LOGINS_BY_IP[client_ip]
        if now - ts <= LOGIN_WINDOW_SECONDS
    ]
    FAILED_LOGINS_BY_IP[client_ip] = attempts

    if len(attempts) >= MAX_LOGIN_ATTEMPTS:
        flash("Too many login attempts. Please try again in a few minutes.", "error")
        return redirect(url_for('auth.login'))

    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if not email or not password:
        flash("Email and password are required", "error")
        return redirect(url_for('auth.login'))

    user = get_user_by_email(email)
    if not user or not verify_password(password, user['password_hash']):
        FAILED_LOGINS_BY_IP[client_ip].append(now)
        flash("Invalid email or password", "error")
        return redirect(url_for('auth.login'))

    if not user['is_active']:
        FAILED_LOGINS_BY_IP[client_ip].append(now)
        flash("Your account has been deactivated", "error")
        return redirect(url_for('auth.login'))

    FAILED_LOGINS_BY_IP.pop(client_ip, None)

    dev = get_developer_by_user_id(user['user_id'])

    session['user_id'] = user['user_id']
    session['email'] = user['email']
    session['role'] = user['role']
    
    if dev:
        session['full_name'] = dev['full_name']
        session['developer_id'] = dev['developer_id']
    else:
        session['full_name'] = "System Admin"
        session['developer_id'] = 0

    if user['role'] == 'admin':
        flash("Admin Access Granted", "success")
        return redirect(url_for('admin.panel'))

    flash("Welcome back!", "success")
    return redirect(url_for('dashboard.index'))

@bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('auth.login'))