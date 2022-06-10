"""Server for final project app."""
import os
from flask import Flask, render_template, request, jsonify, redirect #webbrowser
#imported additionally 06/31 - redirect and webbrowser(ERROR shows) in order
#to redirect to a NPS campground site 
#and open a new tab
import crud
import requests

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

API_KEY = os.environ['NPS_KEY']

@app.route('/')
def homepage():
    """returns home page"""
    
    return render_template ("homepage.html")
    #homepage is where user logs-in or can create an account
    #sign-in with gmail or facebook option (is this an extra time thing?)

#create a new user
@app.route("/users", methods=["POST", "GET"])
def register_user():
    """Registers a new user to the db."""

    first_name = request.form.get("first_name")
    last_name=request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    #checking to see if the user already exists
    #if there is no email, is user = null??
    if user: #True if user exists
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created!")
        
    user_id = crud.get_user_id(email)
    #use the functions in crud.py to find the user id


    return redirect("/users/user_id", user_id=user_id)



@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")
    

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")



    redirect("/users/<user_id>", user_id=user.user_id)


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show saved campsites and profile of a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_account.html", user=user)


@app.route('/create_account')
def create_account():
    """create an account for the user"""

    return render_template ("create_account.html")

@app.route('/search')
def search():
    """displays the search page with form"""

    return render_template ("search.html")

#ROUTE to the NPS web page of campsite
# @app.route('/campground/<campground_url>')
# def view_campground(campground_url):
#     """displays specific NPS campground webpage"""

#     return redirect("campground_url", code=302)

#ROUTE to a new web page passing through the campground_id

@app.route('/campground/<campground_id>/<user_id>')
def view_campground(campground_id):
    """passes through the campground id"""
    #how do I pass through the user_id as well?
    #I think I need this to save to their user_page??

    return render_template ("search_results.html", campground_id=campground_id)


@app.route('/search_state')
def find_campgrounds():
    """Search for campgrounds on NPS"""

    state = request.args.get('state', '')

    url = f'https://developer.nps.gov/api/v1/campgrounds?stateCode={state}&limit=100&api_key={API_KEY}'

    response = requests.get(url)
    
    data = response.json()

    return data


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )
