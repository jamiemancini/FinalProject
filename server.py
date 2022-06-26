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
    return redirect("/")

@app.route('/')
def homepage():
    """returns home page"""

    flash('Welcome to the Homepage')
    print("homepage route")
    return render_template ("homepage.html")
    

@app.route('/login_page')
def login_page():
    """returns login page"""

    print("login route")
    return render_template('login-page.html')

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login function to retrieve id of user from session if any, and load user into memory"""
    
    user=User.query.filter_by(user_id=user_id).first()

    return user

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """log user in and add user to session"""
    
    email = request.form.get('email')
    print(email)
    password = request.form.get('password')
    print(password)
    user=crud.get_user_by_email(email)

    if user:
        if user.check_password(password) is True:
            print("Verified user, welcome back!")
            session['user_id'] = user.user_id
            print(f"The user-id is: {user.user_id}")
            flash('Login completed')
            return redirect(f"/users/{user.user_id}")
        else:
            print(user.user_id)
            flash('Invalid password, please try again.')
            print("did not verify user")
            return redirect('login_page')

    else:
        print("does not exist")
        flash('Sorry, this user does not exit. Please try again')
        return redirect('/login_page')



@app.route("/users", methods=["POST", "GET"])
def register_user():
   
    """Registers a new user to the db."""

    print("We are creating a user!")
    first_name = request.form.get("first_name")
    last_name=request.form.get("last_name")
    email = request.form.get("email")
    password_hash = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if user: 
        flash('Cannot create an account with that email. Try again.')
    else:
        user = crud.create_user(first_name, last_name, email, password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! Welcome {email}')
        
    user = crud.get_user_by_email(email)
    #use the functions in crud.py to find the user id
    print("user_id: ", user.user_id)
    session['user_id'] = user.user_id

    return redirect(f"/users/{user.user_id}")



@app.route("/users/<user_id>", methods=["POST", "GET"])
def show_user(user_id):
    """Show saved campsites and profile of a particular user."""

    user = crud.get_user_by_id(user_id)
    rating=crud.get_rating_by_user_id(user_id)
    
    print("*********route to user's homepage")
    print(f"The logged in user_id is: {user}")
    print(f"The logged in ratings are: {rating}")
    
    return render_template("user_account.html", user=user, rating=rating)


@app.route('/create_account')
def create_account():
    """create an account for the user"""

    return render_template("create_account.html")

@app.route('/search')
def search():
    """displays the search page with form"""
    print("found user id: ", session.get('user_id', None))    
    return render_template("search.html")

@app.route('/<campground_id>')
def view_campground(campground_id):
    """passes through the campground id"""

    user_id = session.get("user_id", None)
    print(f"THIS is the user's ID: {user_id}")
    print(f"this is the campground ID {campground_id}")

    if user_id == None:
        user = crud.create_user("Guest", "Guest", "Guest", "Guest")
        print(f"IF: THIS is the user's ID: {user_id}")
    
    
    else:
        user = crud.get_user_by_id(user_id)
        print(f"THIS is the user: {user}")
        print(user.first_name)
        print(user.last_name)
    
    url = f'https://developer.nps.gov/api/v1/campgrounds?stateCode=&limit=1&q={campground_id}&api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    rating = crud.get_rating_by_camping_id(campground_id)

    print(data)
    # print(data['data'][0]['parkCode'])
    park_name = find_park_name(data['data'][0]['parkCode'])
    print(park_name)
    
    return render_template ("search_results.html", rating=rating, campground_id=campground_id, user=user, user_id=user_id, campground_data=data, park_name=park_name)

@app.route('/save_reviews', methods = ["POST", "GET"])
def save_review():
    """creates a review by user"""
    user_id = session.get("user_id", None)
    print(user_id)
    campground_id=request.form.get("campground_id")
    print(campground_id)
    description=request.form.get("description")
    score=request.form.get("score")
    
    rating = crud.create_rating(user_id,campground_id,description,score)
    print(campground_id)

    db.session.add(rating)
    db.session.commit()

    # flash('Review saved')
    return redirect(f"/{campground_id}")
    
    #, user_id=user_id, description=description,score=score, campground_id=campground_id)

# @app.route('/save_campsite', methods = ["POST"])
# def save_campsite():
#     """saves campsite to their account"""

#     user_id = request.form.get("user_id")
#     campground_id=request.form.get("campground_id")
#     trip_plans=request.form.get("trip_plans")
#     season=request.form.get("season")
#     print(season)
#     # rating = crud.create_rating(user_id,campground_id,description,score)

#     # db.session.add(rating)
#     # db.session.commit()

#     flash('Travel Ideas have been saved to your account!')

#     return print("testing this form")


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
    print(data)
    return data


if __name__ == "__main__":
    connect_to_db(app)
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )
