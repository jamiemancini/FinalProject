"""Server for final project app."""
import os
from flask import Flask, render_template, request, jsonify

#only import what you need the server to access


import requests
#commented out above bec/
# ModuleNotFoundError: No module named 'requests'
#tried: pip3 install requests in terminal

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'
# app.jinja_env.undefined=StrictUndefined

API_KEY = os.environ['NPS_KEY']
print(API_KEY)

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


#should I be using state, because the input of my form has value="state"
@app.route('/search_state')
def find_campgrounds():
    """Search for campgrounds on NPS"""

    #is this getting it from the form, where the value is state
    state = request.args.get('state', '')
    

    url = f'https://developer.nps.gov/api/v1/campgrounds?stateCode={state}&api_key={API_KEY}'
    print(url)

    response = requests.get(url)
    
    data = response.json()
    print(data)

    return data


# @app.route('/create_user')


# @app.route('/login')



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )
