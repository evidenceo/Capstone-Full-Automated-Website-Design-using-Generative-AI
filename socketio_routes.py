from flask_socketio import emit
from init_nodes import init_nodes
from models import WebsiteTemplate, Page


def register_socketio_events(socketio, state_manager, flow_manager):
    @socketio.on('request_template')
    def handle_template_request(data):
        template_type = data['type']
        template = WebsiteTemplate.query.filter_by(name=template_type, is_base_template=True).first()
        if template:
            # Store the template type and template ID for global access
            state_manager.store_data('template_type', template_type)
            state_manager.store_data('template_id', template.id)

            initial_page = fetch_initial_page_content(template.id)
            if initial_page:
                # Match the property names with those expected by the client
                emit('template_response', {'initialPageContent': initial_page, 'templateId': template.id})
            else:
                emit('template_response', {'error': "Initial page content not found"})
        else:
            emit('template_response', {'error': "Template not found"})

    def fetch_initial_page_content(template_id):
        # Example: Fetch the 'home' page of the template
        page = Page.query.filter_by(template_id=template_id, page_name='Home').first()
        if page:
            return page.html_content
        return None

    @socketio.on('set_template_type')
    def handle_set_template_type(data):
        template_type = data.get('type')
        state_manager.store_data('template_type', template_type)

    @socketio.on('start_conversation')
    def handle_start():
        # Assuming you have a way to determine the initial node or message
        initial_node_name = "WelcomeNode"
        state_manager.set_current_node(initial_node_name)
        # Process the initial input or simply trigger the initial message
        flow_manager.process_input()

    @socketio.on('user_response')
    def handle_user_response(data):
        user_input = data.get('message')
        # Here you process the user's input and determine the next steps
        flow_manager.process_input(user_input=user_input)

    # Initialize nodes
    init_nodes(flow_manager)
