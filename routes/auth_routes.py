from flask import Blueprint, render_template, request, redirect, session, url_for
from database.models import User
from database.db import db

auth_bp = Blueprint('auth', __name__)


# ---------------- LOGIN ----------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:
            session['user_id'] = user.id
            return redirect(url_for('main.home'))
        else:
            return "❌ Invalid username or password"

    return render_template('auth/login.html')


# ---------------- SIGNUP ----------------
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        # ✅ check if user already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "⚠️ Username already exists"

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')


# ---------------- LOGOUT ----------------
@auth_bp.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('auth.login'))

