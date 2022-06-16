"""Server for final project app."""

from model import User
from flask import Flask, render_template, request, jsonify, redirect, session, flash 
#webbrowser
#imported additionally 06/31 - redirect and webbrowser(ERROR shows) in order
#to redirect to a NPS campground site 
#and open a new tab
import os
import crud
import requests
import json
from model import connect_to_db, db
from flask_login import LoginManager, current_user, login_user, logout_user, login_required


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

login_manager = LoginManager(app)
login_manager.login_view = '/login_page'

API_KEY = os.environ['NPS_KEY']

@app.route('/')
def homepage():
    """returns home page"""
    
    return render_template ("homepage.html")
    

@app.route('/login_page')
def login_page():
    """Show login and create account page"""
    return render_template('login-page.html')

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login function to retrieve id of user from session if any, and load user into memory"""
    user=User.query.filter_by(user_id=user_id).first()

    return user

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """log user in and add user to session"""

    if current_user.is_authenticated:
        return redirect ('/')

    email = request.form.get('email')
    password = request.form.get('password')

    user=crud.get_user_by_email(email)

    if user:
        if user.check_password(password)==True:
            # login_user(user)
            print("verified user")
            session['user_id'] = user.user_id
            return redirect(f"/users/{user.user_id}")
        else:
            flash('Invalid password')
            print("did not verify user")
            return redirect('/login-page.html')

    else:
        print("does not exist")
        flash('Sorry, this user does not exit.')
        return redirect('login-page.html')



@app.route("/users", methods=["POST", "GET"])
def register_user():
   
    """Registers a new user to the db."""
    print("We are creating a user!")
    first_name = request.form.get("first_name")
    last_name=request.form.get("last_name")
    email = request.form.get("email")
    password_hash = request.form.get("password")

    user = crud.get_user_by_email(email)
    #checking to see if the user already exists
    #if there is no email, is user = null??
    
    if user: #True if user exists
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password_hash)
        db.session.add(user)
        db.session.commit()
        flash("Account created!")
        
    user = crud.get_user_by_email(email)
    #use the functions in crud.py to find the user id
    print("user_id: ", user.user_id)
    session['user_id'] = user.user_id

    return redirect(f"/users/{user.user_id}")


#06/13 removed the following login because updated to using flask_login
# @app.route("/login", methods=["POST"])
# def process_login():
#     """Process user login."""

#     email = request.form.get("email")
#     password = request.form.get("password")
    

#     user = crud.get_user_by_email(email)
#     if not user or user.password != password:
#         flash("The email or password you entered was incorrect.")
#     else:
#         # Log in user by storing the user's email in session
#         session["user_email"] = user.email
#         flash(f"Welcome back, {user.email}!")



#     redirect("/users/<user_id>", user_id=user.user_id)


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show saved campsites and profile of a particular user."""

    user = crud.get_user_by_id(user_id)
    print(user)
    return render_template("user_account.html", user=user)


@app.route('/create_account')
def create_account():
    """create an account for the user"""

    return render_template("create_account.html")

@app.route('/search')
def search():
    """displays the search page with form"""
    print("found user id: ", session.get('user_id', None))    
    return render_template("search.html")

#ROUTE to the NPS web page of campsite
# @app.route('/campground/<campground_url>')
# def view_campground(campground_url):
#     """displays specific NPS campground webpage"""

#     return redirect("campground_url", code=302)

#ROUTE to a new web page passing through the campground_id

#06/10 - took out /campground/ because I was getting a 404 error
#"GET /campground/static/wecamp.js HTTP/1.1" 404 -
#I also removed it from fetch-app.js
@app.route('/<campground_id>')
def view_campground(campground_id):
    """passes through the campground id"""
    user_id = session.get("user_id", None)
    url = f'https://developer.nps.gov/api/v1/campgrounds?stateCode=&limit1&q={campground_id}&api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    print("cambround data: ", data)

    return render_template ("search_results.html", campground_id=campground_id, user_id=user_id, campground_data=data)

@app.route('/save_reviews', methods = ["POST"])
def save_review():
    """creates a review by user"""
    user_id = session.get("user_id", None)
    campground_id=request.form.get("campground_id")
    description=request.form.get("description")
    score=request.form.get("score")
    
    rating = crud.create_rating(user_id,campground_id,description,score)

    db.session.add(rating)
    db.session.commit()

    return redirect(f"/{campground_id}")



@app.route('/search_campground')
def find_campground_by_id(campground_id):
    """Search for specific NPS campgrounds using its ID"""

    #campground_id = request.args.get('campground_id', '')
    # state = request.args.get('state', '')

    url = f'https://developer.nps.gov/api/v1/campgrounds?stateCode=&limit1&q={campground_id}&api_key={API_KEY}'

    response = requests.get(url)
    
    data = response.json()

    return data

@app.route('/search_state')
def find_campgrounds():
    """Search for campgrounds on NPS"""

    state = request.args.get('state', '')

    url = f'https://developer.nps.gov/api/v1/campgrounds?stateCode={state}&limit=100&api_key={API_KEY}'

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
