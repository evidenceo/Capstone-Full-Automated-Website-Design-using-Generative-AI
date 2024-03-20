from threading import Timer
from models import db, Page


class ServiceLocator:
    _services = {}

    @classmethod
    def register_service(cls, name, instance):
        cls._services[name] = instance

    @classmethod
    def get_service(cls, name):
        return cls._services.get(name)


# Class to Handle State of the conversation
class StateManager:
    def __init__(self):
        self.current_node = None
        self.data = {}

    def set_current_node(self, node):
        self.current_node = node

    def get_current_node(self):
        return self.current_node

    def store_data(self, key, value):
        self.data[key] = value

    def retrieve_data(self, key):
        return self.data.get(key)


# Abstract representation of a conversation step
class Node:
    def __init__(self, name, next_node=None):
        self.name = name
        self.next_node = next_node

    def process(self, state_manager, user_input=None):
        raise NotImplementedError("Each node must implement its process method.")


class DBUtils:
    @staticmethod
    def update_template_in_db(template_id, page_name, updated_content, content_type):
        page = Page.query.filter_by(template_id=template_id, page_name=page_name).first()

        if page:
            if content_type == 'html':
                page.html_content = updated_content
            elif content_type == 'css':
                page.css_content = updated_content
            elif content_type == 'js':
                page.js_content = updated_content
            else:
                raise ValueError("Unsupported content type")

            db.session.commit()
        else:
            raise Exception("Page not found")


# Manage the flow of the conversation
class FlowManager:
    def __init__(self, state_manager, socketio):
        self.state_manager = state_manager
        self.nodes = {}
        self.socketio = socketio

    def add_node(self, node: object) -> object:
        self.nodes[node.name] = node

    def process_input(self, user_input=None):
        current_node_name = self.state_manager.get_current_node()
        if current_node_name not in self.nodes:
            raise Exception("Current node not found in flow.")

        current_node = self.nodes[current_node_name]
        print(f"Flow:{current_node}")  # Debug
        result = current_node.process(self.state_manager, user_input)
        print(f"result:{result}")  # debug

        if 'message' and 'response_type' in result:
            self.socketio.emit('conversation_update', result)

        if 'next_node' in result and not result.get('auto_progress', False):
            self.state_manager.set_current_node(result['next_node'])

        # Automatically progress to the next node if needed
        if 'next_node' in result:
            if result.get('auto_progress', False):
                # If auto_progress is True, delay the progression
                self.schedule_auto_progress(result['next_node'], delay=2)  # delay in seconds
            else:
                self.state_manager.set_current_node(result['next_node'])

    def schedule_auto_progress(self, next_node_name, delay):
        """Schedule automatic progression to the next node after a delay."""
        Timer(delay, self.auto_progress, args=[next_node_name]).start()

    def auto_progress(self, next_node_name):
        """Automatically progress to the next node."""
        self.state_manager.set_current_node(next_node_name)
        # Process the next node; since user_input is None, it initiates the node's action without waiting for input
        self.process_input()
