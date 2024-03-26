from flask import Blueprint, render_template, request, url_for, redirect, jsonify, session, flash
from flask_login import login_required, login_user, current_user
from werkzeug.security import check_password_hash
from models import db, User, TemplateCategory, WebsiteTemplate, UserTemplate, UserTemplatePage
from conversation_flows.flow_mapping import ConversationFlowMapping
from classes import ServiceLocator

# Create a Blueprint for your HTTP routes
http_routes = Blueprint('http_routes', __name__)


@http_routes.route('/')
def index():
    return render_template("home.html")


@http_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return jsonify({'error': 'You are already logged in.'}), 403

    if request.method == 'POST':
        data = request.json
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already in use.'}), 409

        new_user = User(first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)  # Set password hash

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': 'Account created successfully!'}), 201

    return render_template('register.html')


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
    # Fetch user id
    user_id = current_user.id
    user_templates = UserTemplate.query.filter_by(user_id=user_id).all()
    return render_template('user_dashboard.html', user_templates=user_templates)


@http_routes.route('/templates')
def templates():
    categories = TemplateCategory.query.all()
    return render_template('templates.html', categories=categories)


@http_routes.route('/conversation/<int:template_id>')
@login_required
def conversation(template_id):
    # Retrieve flow manager because we'd be using it here
    flow_manager = ServiceLocator.get_service('flow_manager')
    state_manager = ServiceLocator.get_service('state_manager')

    # Fetch the template from the database
    template = WebsiteTemplate.query.get(template_id)
    if template is None:
        return "Template not found", 404

    # Fetch user id
    user_id = current_user.id

    # Then duplicate the template for the user
    user_template = UserTemplate(
        user_id=user_id,
        original_template_id=template.id,
        name=template.name,  # Allow users to rename
        status='in progress'
    )
    db.session.add(user_template)
    db.session.commit()

    # Duplicate the pages of the template
    for page in template.pages:
        if template_id == page.template_id:
            user_page = UserTemplatePage(
                user_template_id=user_template.id,
                page_name=page.page_name,
                modified_html=page.html_content,
                modified_css=page.css_content,
                modified_js=page.js_content
            )
            db.session.add(user_page)
    db.session.commit()

    # Store the user's template id in state_manager
    state_manager.store_data('user_template_id', user_template.id)

    # determine the conversation flow based on the template's category
    category_name = template.category.name

    # Use ConversationFlowMapping to get the appropriate conversation flow initializer
    conversation_flow_initializer = ConversationFlowMapping.get_flow_initializer(category_name)

    # Load the appropriate conversation flow the template falls under
    if conversation_flow_initializer:
        conversation_flow_initializer(flow_manager)

    # Render the conversation page, passing the template and conversation flow
    return render_template('conversation.html', template=template, user_template_id=user_template.id)


@http_routes.route('/design_dashboard/<int:user_template_id>')
@login_required
def design_dashboard(user_template_id):
    return render_template('design_dashboard.html', user_template_id=user_template_id)






