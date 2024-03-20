'''
Setup the website authentication routes
'''
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


'''
Setup the website signin route
'''
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle the login form submission
        requestBody = request.form
        email = requestBody['email']
        password = requestBody['password']

        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('pages.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

        return render_template("home.html", user=current_user)
    else:
        # Display the login form
        return render_template("login.html", user=current_user)


'''
Setup the website signout route
'''
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


'''
Setup the website signup route
'''
@auth.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle the Sign Up form submission
        requestBody = request.form
        first_name = requestBody['first_name']
        email = requestBody['email']
        password = requestBody['password']
        confirmPassword = requestBody['confirmPassword']

        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        if len(first_name) < 2:
            flash('First Name must be greater than 2 characters', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters', category='error')
        elif password != confirmPassword:
            flash('Passwords do not match', category='error')
        else:
            new_user = Users(email=email, 
                             first_name=first_name, 
                             password=generate_password_hash(password, method='scrypt', salt_length=16))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('pages.home'))

        return render_template("home.html", user=current_user)
    else:
        # Display the login form
        return render_template("signup.html", user=current_user)

