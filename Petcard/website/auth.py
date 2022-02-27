from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from . import db 
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/", methods=['POST', 'GET'])
@auth.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email is incorrect.', category='error')
    
    return render_template("login.html", user=current_user)
    

@auth.route("/signin", methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form.get("username").title()
        email = request.form.get("email")
        password = request.form.get("password")
        passwordConfirm = request.form.get("passwordConfirm")
        
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password != passwordConfirm:
            flash('Password don\'t match.', category='error')
        elif len(username) < 3:
            flash('Username is too short.', category='error')
        elif len(password) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash('Email is invalid.', category='error')            
        else:
            new_user = User(username=username, email=email, 
                            password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User created!', category='sucess')
            return redirect(url_for('views.register'))
    
    return render_template("signin.html", user=current_user)
    
    
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    return(redirect(url_for('auth.login')))
