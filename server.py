"""Server for final project app."""

from flask import Flask, render_template, request, jsonify

import os
import requests

app = Flask(__name__)

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# API_KEY = os.environ['NPS_KEY']

@app.route('/')
def homepage():
    """returns home page"""
    
    return render_template ("homepage.html")
    #homepage is where user logs-in or can create an account
    #sign-in with gmail or facebook option (is this an extra time thing?)

@app.route('/search')
def search():
    """returns the search page"""

    return render_template ("search.html")
    #search is where the user will search using the API to find campsites that meet specific criteria

# @app.route('/create_user')


# @app.route('/login')



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )
