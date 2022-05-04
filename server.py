"""Server for final project app."""

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def homepage():
    return "homepage goes here"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )
