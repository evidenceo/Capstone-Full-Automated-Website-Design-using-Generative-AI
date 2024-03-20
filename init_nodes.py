from concrete_nodes import *


def init_nodes(flow_manager):
    # Define and add nodes
    welcome_node = WelcomeNode("WelcomeNode", "GetWebsiteName")
    get_website_name_node = GetWebsiteName("GetWebsiteName", "GetBusinessGoal")
    get_business_goal = GetBusinessGoal("GetBusinessGoal", "GetWebsiteTheme")
    get_website_theme = GetWebsiteTheme("GetWebsiteTheme", "SetWebsiteTheme")
    set_website_theme = SetWebsiteTheme("SetWebsiteTheme", None)
    flow_manager.add_node(welcome_node)
    flow_manager.add_node(get_website_name_node)
    flow_manager.add_node(get_business_goal)
    flow_manager.add_node(get_website_theme)
    flow_manager.add_node(set_website_theme)
    # Add more nodes here
