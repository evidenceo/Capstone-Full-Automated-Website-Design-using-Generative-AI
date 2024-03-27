from .ecommerce.init_nodes import init_ecommerce_nodes
from .portfolio.init_nodes import init_portfolio_nodes
from .events.init_nodes import init_events_nodes


class ConversationFlowMapping:
    mapping = {
        'ecommerce': init_ecommerce_nodes,
        'portfolio': init_portfolio_nodes,
        'events': init_events_nodes
    }

    @staticmethod
    def get_flow_initializer(category_name):
        """
                Returns the conversation flow initializer function based on the template category name.

                Args:
                    category_name (str): The name of the template category.

                Returns:
                    Function: A function that initializes the conversation flow for the given category.
                              Returns None if no mapping is found for the category name.
                """
        return ConversationFlowMapping.mapping.get(category_name)
