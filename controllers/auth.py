from flask import Flask,session,Blueprint,request,render_template,redirect,url_for
from models.user import create_user, get_user_by_email, create_developer_profile, verify_password

bp = Blueprint('auth',__name__)

@bp.route('/register', methods=['GET','POST'])
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

    
    existing_user = get_user_by_email(email)
    if existing_user:
        return render_template('auth/register.html', error="email already exists!")
    
    if not email or '@' not in email:
        return render_template('auth/register.html', error="Invalid email address")
    
    if(not password or len(password)<12):
         return render_template('auth/register.html', error="Invalid Password")
     
    if not bio or not contact_link or not location:
         return render_template('auth/register.html', error="incomplete information")
     
    user_id = create_user(email,password)
    create_developer_profile(user_id,full_name,bio,location,years_experience,contact_link)
    
    session['user_id'] = user_id
    session['email'] = email
    session['role'] = 'developer'
    
    return render_template('dashboard/dashboard.html')
    # return redirect(url_for('dashboard.index'))

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    
    if not email or not password:
        return render_template('auth/login.html',error='Email or password not entered')
    
    user = get_user_by_email(email)
    if not user:
        return render_template('auth/login.html',error='email does not exist')
    
    if not verify_password(password,user[2]):
        return render_template('auth/login.html',error='incorrect password')
    
    if not user[5]:
        return render_template('auth/login.html',error="account is deactivated, contact support for info")

    session['user_id'] = user[0]
    session['email'] = email[1]
    session['role'] = user[3]
    
    if user[3] == 'admin':
        return redirect(url_for('admin.panel'))
    
    return render_template('dashboard/dashboard.html')
    # return redirect(url_for('dashboard.index'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))