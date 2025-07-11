from app.extensions import db
from app.forms import LoginForm
from app.models import User, GoogleAccount
from app.utils.google_auth import get_google_auth_url, exchange_code_for_tokens
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
import requests

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("main.index"))
        flash("Invalid email or password.")
    return render_template("login.html", form=form)

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route("/auth/google_login")
def google_login():
    auth_url = get_google_auth_url()
    return redirect(auth_url)

@auth_bp.route("/auth/google_callback")
def google_callback():
    code = request.args.get("code")
    if not code:
        return "Missing code", 400

    tokens = exchange_code_for_tokens(code)
    refresh_token = tokens.get("refresh_token")
    access_token = tokens.get("access_token")
    expires_in = tokens.get("expires_in")

    from datetime import datetime, timedelta
    token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)

    userinfo = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    google_id = userinfo.get("id")
    email = userinfo.get("email")

    google_account = GoogleAccount.query.filter_by(user_id=current_user.id).first()
    if google_account:
        google_account.google_id = google_id
        google_account.email = email
        google_account.access_token = access_token
        google_account.refresh_token = refresh_token
        google_account.token_expiry = token_expiry
    else:
        google_account = GoogleAccount(
            user_id=current_user.id,
            google_id=google_id,
            email=email,
            access_token=access_token,
            refresh_token=refresh_token,
            token_expiry=token_expiry
        )
        db.session.add(google_account)

    db.session.commit()
    return redirect(url_for("main.index"))