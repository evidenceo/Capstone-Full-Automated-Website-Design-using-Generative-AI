from concrete_nodes import *


def init_nodes(flow_manager):
    # Define and add nodes
    welcome_node = WelcomeNode("WelcomeNode", "GetInformation")
    get_info_node = GetInformation("GetInformation", "CustomizeTemplate")
    customize_temp_node = CustomizeTemplate("CustomizeTemplate", "DetermineNextStep")
    determine_next_node = DetermineNextStep("DetermineNextStep", None)
    flow_manager.add_node(welcome_node)
    flow_manager.add_node(get_info_node)
    flow_manager.add_node(customize_temp_node)
    flow_manager.add_node(determine_next_node)
    # Add more nodes here
