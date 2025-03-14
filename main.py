import os
from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_cors import CORS
from models import db, User
from routes import http_routes
from template_routes import template_blueprint
from socketio_routes import register_socketio_events
from classes import StateManager, FlowManager, ServiceLocator
from chatbot_classes import template_bot, text_bot


def create_app():
    # Create a Flask web application instance
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins=["http://127.0.0.1:5001"])
    CORS(app)
    app.secret_key = os.urandom(24)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Define the user loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    app.register_blueprint(http_routes)
    app.register_blueprint(template_blueprint)

    # Configure the SQLAlchemy part of the app instance
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Initialize the database with the Flask app

    # Configure folder for uploading images as part of the app instance
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

    # Initialize flow and state manager
    state_manager = StateManager()
    flow_manager = FlowManager(app, state_manager, socketio)

    # Initialize service Locator
    ServiceLocator.register_service('socketio', socketio)
    ServiceLocator.register_service('template_bot', template_bot)
    ServiceLocator.register_service('text_bot', text_bot)
    ServiceLocator.register_service('flow_manager', flow_manager)
    ServiceLocator.register_service('state_manager', state_manager)

    # Register socketio events
    register_socketio_events(socketio, state_manager, flow_manager)

    return app, socketio


if __name__ == '__main__':
    app, socketio = create_app()
    if not os.path.exists('instance/mydatabase.db'):
        with app.app_context():
            db.create_all()  # Only run once to create database tables

    socketio.run(app, port=5001, debug=True, allow_unsafe_werkzeug=True)
