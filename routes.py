from flask import Blueprint, render_template

# Create a Blueprint for your HTTP routes
http_routes = Blueprint('http_routes', __name__)


@http_routes.route('/')
def index():
    return render_template("index.html")


@http_routes.route('/builder', methods=['GET'])
def builder():
    return render_template("builder.html")


@http_routes.route('/main')
def main():
    return render_template("main.html")
