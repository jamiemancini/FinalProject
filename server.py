"""Server for final project app."""
import os
from flask import Flask, render_template, request, jsonify, redirect #webbrowser
#imported additionally 06/31 - redirect and webbrowser(ERROR shows) in order
#to redirect to a NPS campground site 
#and open a new tab

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

@app.route('/search')
def search():
    """displays the search page with form"""

    return render_template ("search.html")

@app.route('/campground/<campground_url>')
def view_campground(campground_url):
    """displays specific NPS campground webpage"""

    return redirect("campground_url", code=302)

# @app.route('/campground/<campground_id>')
# def view_campground(campground_id):
#     """passes through the campground id"""

#     return campground_id


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
