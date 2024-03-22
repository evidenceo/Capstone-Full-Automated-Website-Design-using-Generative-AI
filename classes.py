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
        self.current_step = None
        self.data = {}

    def set_current_node(self, node):
        self.current_node = node

    def get_current_node(self):
        return self.current_node

    def set_current_step(self, step):
        self.current_step = step

    def get_current_step(self):
        return self.current_step

    def store_data(self, key, value):
        self.data[key] = value

    def retrieve_data(self, key):
        return self.data.get(key)


# Abstract representation of a conversation step
class Node:
    def __init__(self, name, next_node=None, requires_input=True):
        self.name = name
        self.next_node = next_node
        self.requires_input = requires_input

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
    def __init__(self, app, state_manager, socketio):
        self.app = app
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

        if current_node.requires_input or user_input is not None:
            # For node requires input, it is a synchronous node, so nodes that involve interaction with the user
            self._process_node(current_node, user_input)
        else:
            # For nodes that do not require interaction with the user, asynchronous nodes
            self._process_async_node(current_node)

    def _process_node(self, node, user_input):
        result = node.process(self.state_manager, user_input)
        print(f"result:{result}")  # debug
        self._handle_result(result)

    def _process_async_node(self, node):
        with self.app.app_context():
            result = node.process(self.state_manager)
            self._handle_result(result)

    def _handle_result(self, result):
        if 'message' and 'response_type' in result:
            self.socketio.emit('conversation_update', result)

        if 'next_node' in result:
            self.state_manager.set_current_node(result['next_node'])
            if result.get('auto_progress', False):
                self.schedule_auto_progress(result['next_node'])

        if 'action' in result:
            self.socketio.emit('conversation_update', result)

    def schedule_auto_progress(self, next_node_name):
        """Schedule automatic progression to the next node after a delay."""
        Timer(2, lambda: self._process_async_node(self.nodes[next_node_name])).start()
