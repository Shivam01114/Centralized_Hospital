from flask import Flask, redirect, url_for, session
from database.db import db

# ================= APP INIT =================
app = Flask(__name__)

# ================= CONFIG =================
app.config.from_object("config")
app.config['SECRET_KEY'] = 'shivam_secret_key_2026'


# ================= INIT DB =================
db.init_app(app)


# ================= IMPORT ROUTES =================
# ⚠️ IMPORTANT: db init ke baad hi import karo
from routes.auth_routes import auth_bp
from routes.main_routes import main_bp
from routes.heart_routes import heart_bp
from routes.liver_routes import liver_bp


# ================= REGISTER BLUEPRINTS =================
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(heart_bp)
app.register_blueprint(liver_bp)


# ================= DEFAULT ROUTE PROTECTION =================
@app.route('/')
def root():
    # ✅ LOGIN CHECK
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))

    return redirect(url_for('main.home'))


# ================= CREATE TABLES =================
with app.app_context():
    db.create_all()


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)