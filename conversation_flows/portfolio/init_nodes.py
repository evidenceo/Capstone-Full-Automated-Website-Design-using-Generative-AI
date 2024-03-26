from conversation_flows.portfolio.portfolio_flow import *


def init_portfolio_nodes(flow_manager):
    # Define and add nodes
    welcome_node = WelcomeNode("WelcomeNode", "GetInformation")
    get_info_node = GetInformation("GetInformation", "CustomizeTemplate")
    customize_temp_node = CustomizeTemplate("CustomizeTemplate", "DetermineNextStep")
    pass
    # Add more nodes here
