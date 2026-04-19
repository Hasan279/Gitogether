from flask import Flask,redirect,url_for
from config import SECRET_KEY, DEBUG

app = Flask(__name__)
app.secret_key = SECRET_KEY

from controllers import auth, dashboard, projects, developers, requests, matches, ratings, admin

app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
# app.register_blueprint(projects.bp)
# app.register_blueprint(developers.bp)
# app.register_blueprint(requests.bp)
# app.register_blueprint(matches.bp)
# app.register_blueprint(ratings.bp)
# app.register_blueprint(admin.bp)

@app.route('/')
def home():
    return redirect(url_for('auth.login'))
if __name__ == "__main__":
    app.run(debug=DEBUG)