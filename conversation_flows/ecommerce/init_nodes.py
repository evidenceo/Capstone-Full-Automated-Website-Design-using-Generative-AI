from conversation_flows.ecommerce.ecommerce_flow import *


def init_ecommerce_nodes(flow_manager):
    # Define and add nodes
    welcome_node = WelcomeNode("WelcomeNode", "GetInformation")
    get_info_node = GetInformation("GetInformation", "CustomizeTemplate")
    customize_temp_node = CustomizeTemplate("CustomizeTemplate", "DetermineNextStep")
    determine_next_node = DetermineNextStep("DetermineNextStep", "HomePage")
    home_page_node = HomePage("HomePage", "AboutPage")
    about_page_node = AboutPage("AboutPage", "ProductPage")
    product_page_node = ProductPage("ProductPage", "ContactPage")
    contact_page_node = ContactPage("ContactPage", "FinalMessage")
    final_message_node = FinalMessage("FinalMessage", None)

    flow_manager.add_node(welcome_node)
    flow_manager.add_node(get_info_node)
    flow_manager.add_node(customize_temp_node)
    flow_manager.add_node(determine_next_node)
    flow_manager.add_node(home_page_node)
    flow_manager.add_node(about_page_node)
    flow_manager.add_node(contact_page_node)
    flow_manager.add_node(product_page_node)
    flow_manager.add_node(final_message_node)
    # Add more nodes here
