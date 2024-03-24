from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from flask_login import login_required, login_user
from werkzeug.security import check_password_hash
from models import db, User, TemplateCategory, WebsiteTemplate

# Create a Blueprint for your HTTP routes
http_routes = Blueprint('http_routes', __name__)


@http_routes.route('/')
def index():
    return render_template("index.html")


@http_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(
            url_for('http_routes.user_dashboard'))  # Change to the user dashboard page if user is already logged in

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already in use.')
            return redirect(url_for('http_routes.signup'))

        new_user = User(first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)  # Set password hash

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!')
        return redirect(url_for('http_routes.login'))  # Redirect to login page after signup

    return render_template('signup.html')


@http_routes.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(
            url_for('http_routes.user_dashboard'))  # Change to the user dashboard page if user is already logged in

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('http_routes.user_dashboard'))  # Move to user dasboard page
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('login.html')


@http_routes.route('/user_dashboard')
@login_required
def user_dashboard():
    # You would typically fetch user's templates from the database
    user_templates = get_user_templates()  # This is a placeholder function
    return render_template('user_dashboard.html', templates=user_templates)


def get_user_templates():
    # Placeholder function - you should implement database logic here
    # From the database, if there are any modified templates in user section it should show here
    return [
        {'name': 'Template 1', 'thumbnail': 'path_to_image', 'edit_url': 'edit_template_url'},
        {'name': 'Template 2', 'thumbnail': 'path_to_image', 'edit_url': 'edit_template_url'},
        # Add as many templates as the user has
    ]


@http_routes.route('/templates')
def templates():
    categories = TemplateCategory.query.all()
    return render_template('templates.html', categories=categories)


@http_routes.route('/conversation/<int:template_id>')
def main():
    # Fetch the template from the database
    template = WebsiteTemplate.query.get(id)
    if template is None:
        return "Template not found", 404

    # determine the conversation flow based on the template's category
    conversation_flow = determine_conversation_flow(template.category.name)

    # Render the conversation page, passing the template and conversation flow
    return render_template('conversation.html', template=template, conversation_flow=conversation_flow)


@http_routes.route('/builder', methods=['GET'])
def builder():
    return render_template("builder.html")


