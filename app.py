from flask import Flask, redirect, render_template, session, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask_wtf.csrf import CSRFProtect

from config import SECRET_KEY, DEBUG, CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

app = Flask(__name__)
app.secret_key = SECRET_KEY
csrf = CSRFProtect(app)

cloudinary.config(
    cloud_name = CLOUDINARY_CLOUD_NAME,
    api_key = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET
)

from controllers import auth, dashboard, projects, developers, requests, matches, ratings, admin

app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(projects.bp)
app.register_blueprint(developers.bp)
app.register_blueprint(requests.bp)
app.register_blueprint(matches.bp)
app.register_blueprint(ratings.bp)
app.register_blueprint(admin.bp)

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=DEBUG)