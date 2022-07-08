"""Server for wecamp final project app."""

from model import User
from flask import Flask, render_template, request, jsonify, redirect, session, flash 
import os
import crud
from all_NPS import *
import requests
import json
from model import connect_to_db, db
from flask_login import LoginManager, current_user, login_user, logout_user, login_required


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

login_manager = LoginManager(app)
login_manager.login_view = '/login_page'

API_KEY = os.environ['NPS_KEY']

@app.route("/logout")
@login_required
def logout():
    """logs out the user"""

    logout_user()
    session.pop("user, None")
    flash('You have sucessfully logged out.  Goodbye!', "info")
    return redirect("/")


@app.route('/')
def homepage():
    """returns home page"""

    # flash('Welcome to the Homepage', "info")
    return render_template ("homepage.html")


@app.route('/cards')
def cards():
    """NOT PATH sample cards page"""

    flash('Welcome to the cards page')
    return render_template ("card_sample.html")



@login_manager.user_loader
def load_user(user_id):
    """Flask-Login function to retrieve id of user from session if any, and load user into memory"""
    
    user=User.query.filter_by(user_id=user_id).first()
    return user

@app.route('/login_page')
def login_page():
    """returns login page"""

    print("login route")
    return render_template('login-page.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """log user in and add user to session"""
    
    email = request.form.get('email')
    password = request.form.get('password')
    user=crud.get_user_by_email(email)

    if user:
        if user.check_password(password) is True:
            session['user_id'] = user.user_id
            flash('Login completed.  Welcome back!', "success")
            return redirect(f"/users/{user.user_id}")
        else:
            flash('Invalid password, please try again.', "warning")
            return redirect('/login_page')

    else:
        flash('Sorry, this user does not exit. Please try again', "warning")
        return redirect('/login_page')



@app.route("/users", methods=["POST", "GET"])
def register_user():
   
    """Registers a new user to the db."""
    

    if request.form.get("password") != request.form.get("password1"):
        flash('Your passwords did not match.', "warning")
        return redirect('/create_account')

    else:
        first_name = request.form.get("first_name")
        last_name=request.form.get("last_name")
        email = request.form.get("email")
        password_hash = request.form.get("password")

        user = crud.get_user_by_email(email)
        
        if user: 
            flash('Cannot create an account with that email. Try again.', "warning")

        else:
            user = crud.create_user(first_name, last_name, email, password_hash)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created! Welcome {email}', "success")
            
        user = crud.get_user_by_email(email)
        session['user_id'] = user.user_id

        return redirect(f"/users/{user.user_id}")


@app.route("/users/<user_id>", methods=["POST", "GET"])
def show_user(user_id):
    """Show saved campsites and profile of a particular user."""

    print(user_id)
    
    user = crud.get_user_by_id(user_id)
    rating=crud.get_rating_by_user_id(user_id)

    print(user)
    print(rating)
    
    return render_template("user_account.html", user=user, rating=rating)


@app.route('/create_account')
def create_account():
    """create an account for the user"""
    user_id = session.get("user_id", None)
    user = crud.get_user_by_id(user_id)

    if user_id is None or user.first_name is None:
        return render_template("create_account.html")
    else:
        return redirect(f"/users/{user.user_id}")

@app.route('/search')
def search():
    """displays the search page with form"""
       
    return render_template("search.html")

@app.route('/<campground_id>')
def view_campground(campground_id):
    """passes through the campground id"""

    user_id = session.get("user_id", None)

    if user_id is None:
        user = crud.create_user("Guest", "Guest", "Guest", "Guest")
    
    
    else:
        user = crud.get_user_by_id(user_id)
        flash(f"Hi! Camper {user.first_name} {user.last_name}!", "success")
    
    url = f'https://developer.nps.gov/api/v1/campgrounds?stateCode=&limit=1&q={campground_id}&api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    rating = crud.get_rating_by_camping_id(campground_id)

    # park_name = find_park_name(data['data'][0]['parkCode'])
    # print(park_name)
    return render_template ("search_results.html", rating=rating, campground_id=campground_id, user=user, user_id=user_id, campground_data=data)

@app.route('/save_reviews', methods = ["POST", "GET"])
def save_review():
    """creates a review by user"""

    user_id = session.get("user_id", None)
    camp_name=request.form.get("camp_name")
    print(camp_name)
    campground_id=request.form.get("campground_id")
    description=request.form.get("description")
    score=request.form.get("score")
    
    rating = crud.create_rating(user_id,camp_name, campground_id,description,score,)

    db.session.add(rating)
    db.session.commit()

    print("RATING IS SAVED")
    print(rating)
    return redirect(f"/{campground_id}")
    

@app.route('/search_state')
def find_campgrounds():
    """Search for campgrounds on NPS by state"""

    state = request.args.get('state', '')

    if state =='':
        url = f'https://developer.nps.gov/api/v1/campgrounds?limit=650&api_key={API_KEY}'
        response = requests.get(url)
        data = response.json()

    else:
        url = f'https://developer.nps.gov/api/v1/campgrounds?stateCode={state}&limit=650&api_key={API_KEY}'
        response = requests.get(url)
        data = response.json()
    return data


if __name__ == "__main__":
    connect_to_db(app)
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )
