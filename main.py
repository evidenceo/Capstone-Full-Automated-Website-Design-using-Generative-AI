import os
from flask import Flask, render_template, request, session, jsonify
from models import db, WebsiteTemplate, Page
from TestFlow import conversation_flow
from OpenCAI import SessionManager

# Create a Flask web application instance
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize the database with the Flask app

# Global variable to track if the init code has run
has_initialized = False


@app.before_request
def before_request():
    global has_initialized
    if not has_initialized:
        # Initialize the database schema (create tables) only once
        db.create_all()
        has_initialized = True


# Import Blueprints after db and models is created
from template_routes import template_blueprint

# Register Blueprints
app.register_blueprint(template_blueprint)

''''''''''''''''''''''''''''''''''''''''''''' ROUTES '''''''''''''''''''''''''''''''''''''''''''''''''''


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/builder', methods=['GET'])
def builder():
    return render_template("builder.html")


@app.route('/main', methods=['GET'])
def main():
    template_type = request.args.get('type', 'default')  # 'default' is a fallback

    session['website_type'] = template_type

    # Load the original template based on type
    template = WebsiteTemplate.query.filter_by(name=template_type, is_base_template=True).first()

    if template:
        initial_page = fetch_initial_page_content(template.id)
        return render_template("main.html", template_id=template.id, initial_page_content=initial_page)
    else:
        return render_template("main.html", error="Template not found")


def fetch_initial_page_content(template_id):
    # Example: Fetch the 'home' page of the template
    page = Page.query.filter_by(template_id=template_id, page_name='Home').first()
    if page:
        return page.html_content
    return None


@app.route('/conversation', methods=['POST'])
def manage_conversation():
    # Initialize or retrieve the conversation flow from the session
    if 'current_node_name' not in session:
        testFlow = conversation_flow()
        session['current_node_name'] = testFlow.flowStart.nodeName
        testFlow.currentNode = testFlow.flowStart  # Ensure currentNode is initialized
        # Now you can safely generate the initial response
        response = {
            "GeneratedText": testFlow.generateText(),
            "UserInputOptions": testFlow.getUserInputOptions()
        }
    else:
        testFlow = conversation_flow()
        testFlow.set_current_node_by_name(session['current_node_name'])
        user_input = request.json.get('message', '')
        response = testFlow.processNode(user_input)
        session['current_node_name'] = testFlow.currentNode.nodeName

    return jsonify(response)  # Send the response back to the client


@app.route('/receive_content', methods=['POST'])
def receive_content():
    data = request.get_json()
    content = data.get('content')
    targetPage = data.get('targetPage')

    # store the received content in the session
    session_manager = SessionManager(session)
    session_manager.set_content_and_target_page(content, targetPage)

    return jsonify({"status": "Content received"})


@app.route('/continue-conversation', methods=['GET', 'POST'])
def continue_conversation():
    session_manager = SessionManager(session)
    content = session_manager.get_content()
    targetPage = session_manager.get_target_page()

    testFlow = conversation_flow()
    current_node_name = session.get('current_node_name')
    testFlow.set_current_node_by_name(current_node_name)

    # first process node with the content and continue
    response = testFlow.processNode(userResponse="", content=content, targetPage=targetPage)

    return jsonify(response)


# Start the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
