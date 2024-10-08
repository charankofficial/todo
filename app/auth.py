from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import bcrypt
import re  
from app.firebase_connect import get_firestore_client

auth = Blueprint('auth', __name__)
db = get_firestore_client()

def is_valid_password(password):
    if (len(password) < 8 or 
        not re.search(r"[A-Z]", password) or  
        not re.search(r"[a-z]", password) or  
        not re.search(r"[0-9]", password) or 
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)): 
        return False
    return True

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not is_valid_password(password):
            flash('Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, a number, and a special character.', category='error')
            return render_template('signup.html')

        users_ref = db.collection('users')
        existing_user_query = users_ref.where('email', '==', email).get()

        if existing_user_query:
            flash('Email address already exists.', category='error')
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = {
                'email': email,
                'password': hashed_password
            }
            users_ref.add(new_user)
            flash('Account created successfully!', category='success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        users_ref = db.collection('users')
        existing_user_query = users_ref.where('email', '==', email).get()

        if existing_user_query:
            user = existing_user_query[0].to_dict()
            stored_hashed_password = user['password']

            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                session['user_email'] = email  
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Email not found. Please sign up first.', category='error')

    return render_template('login.html')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_email', None)
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))
