from flask_socketio import emit
from models import WebsiteTemplate, Page


def register_socketio_events(socketio, state_manager, flow_manager):
    @socketio.on('start_conversation')
    def handle_start():
        initial_node_name = "WelcomeNode"
        state_manager.set_current_node(initial_node_name)
        # Process the initial input or simply trigger the initial message
        flow_manager.process_input()

    @socketio.on('user_response')
    def handle_user_response(data):
        user_input = data.get('message')
        # Here you process the user's input and determine the next steps
        flow_manager.process_input(user_input=user_input)

