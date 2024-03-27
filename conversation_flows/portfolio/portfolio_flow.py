import random
from classes import Node, ServiceLocator, DBUtils
from models import Page


# Implement specific conversation steps by extending 'Node' class

class WelcomeNode(Node):
    def __init__(self, name, next_node=None, requires_input=False):
        super().__init__(name, next_node, requires_input)

    def process(self, state_manager, user_input=None):
        message = "Welcome to Elaa, your AI web designer! Let's start creating your dream website."
        next_node = "GetInformation"
        response_type = None
        auto_progress = True
        return {'message': message, 'response_type': response_type, 'next_node': next_node,
                'auto_progress': auto_progress}


class GetInformation(Node):
    def __init__(self, name, next_node=None, requires_input=True):
        super().__init__(name, next_node, requires_input)

    def process(self, state_manager, user_input=None):
        # Determine the current step in the process
        current_step = state_manager.get_current_step()

        # manage the flow of thw conversation
        if current_step is None or current_step == "get_website_name":
            # first get website name
            return self.get_website_name(state_manager, user_input)
        elif current_step == "get_portfolio_theme":
            return self.get_portfolio_theme(state_manager, user_input)
        elif current_step == "get_professional_goals":
            return self.get_professional_goals(state_manager, user_input)
        elif current_step == "get_design_elements":
            return self.design_elements(state_manager, user_input)
        else:
            return self.final_interaction(state_manager)

    def get_website_name(self, state_manager, user_input):
        # Get text_bot
        text_bot = ServiceLocator.get_service('text_bot')
        if user_input is None:
            # If there's no user input yet, request for website name
            state_manager.set_current_step("get_website_name")
            message_options = [
                "What would you like to name your website?",
                "Please provide a name for your website.",
                "What would you like to name your portfolio website?"
            ]

            # pick a random message
            message = random.choice(message_options)

            # save message as last_system_message when it is called
            state_manager.store_data('last_system_message', message)

            # set response type for user
            response_type = 'text'

            # reset step
            state_manager.set_current_step(None)

            return {'message': message, 'response_type': response_type}
        else:
            # After getting user input, save and move to the next step
            # retrieve last_system_message
            last_system_message = state_manager.retrieve_data('last_system_message')

            # extract info from user input
            prompt_extraction = (f"Given {last_system_message} and {user_input}. Extract the website name from the "
                                 f"information and save in JSON format. Only output JSON format result without any"
                                 f" additional explanation or text.")
            get_website_name = text_bot.extraction(prompt_extraction)

            print(f"prompt_extraction: {get_website_name}")  # debug

            # save the input
            state_manager.store_data('website_name', get_website_name)

            # move to the next step
            state_manager.set_current_step("get_portfolio_theme")
            return self.process(state_manager)

    def get_portfolio_theme(self, state_manager, user_input):
        # Get text_bot
        text_bot = ServiceLocator.get_service('text_bot')
        if user_input is None:
            message_options = [
                "What is the primary focus of your portfolio?",
                "What field does your portfolio primarily highlight?",
            ]

            # pick a random message
            message = random.choice(message_options)

            # save message as last_system_message when it is called
            state_manager.store_data('last_system_message', message)

            # set response type for user
            response_type = 'text'

            return {'message': message, 'response_type': response_type}
        else:
            # retrieve last_system_message
            last_system_message = state_manager.retrieve_data('last_system_message')

            # extract info from user input
            prompt_extraction = (
                f"Given {last_system_message} and {user_input}. Extract the product the user sells from the "
                f"information and save in JSON format. Only output JSON format result without any additional"
                f"explanation or text.")
            get_portfolio_theme = text_bot.extraction(prompt_extraction)
            print(f"prompt_extraction: {get_portfolio_theme}")  # debug

            # save the input
            state_manager.store_data('portfolio_theme', get_portfolio_theme)
            state_manager.set_current_step("get_professional_goals")
            return self.process(state_manager)

    def get_professional_goals(self, state_manager, user_input):
        # Get text_bot
        text_bot = ServiceLocator.get_service('text_bot')
        if user_input is None:
            message_options = [
                "Awesome!\n What do goals do you have for this website?",
                "Good Good...\n So what are you aiming to achieve with this website?"
            ]

            # pick a random message
            message = random.choice(message_options)

            # save message as last_system_message when it is called
            state_manager.store_data('last_system_message', message)

            # set response type for user
            response_type = 'text'

            return {'message': message, 'response_type': response_type}
        else:
            # retrieve last_system_message
            last_system_message = state_manager.retrieve_data('last_system_message')

            # extract info from user input
            prompt_extraction = (
                f"Given {last_system_message} and {user_input}. Extract the business goals from the "
                f"information and save in JSON format. Only output JSON format result without any additional"
                f"explanation or text.")
            get_professional_goals = text_bot.extraction(prompt_extraction)
            print(f"prompt_extraction: {get_professional_goals}")  # debug

            # save the input
            state_manager.store_data('professional_goals', get_professional_goals)

            state_manager.set_current_step("get_design_elements")
            return self.process(state_manager)

    def design_elements(self, state_manager, user_input):
        # Get text_bot
        text_bot = ServiceLocator.get_service('text_bot')
        if user_input is None:
            message_options = [
                "Almost there!\n Do you have any specific design elements in mind for your website? Or would you like"
                " elaa to choose them based on your preferences?",

                "We're nearly finished! Would you like to suggest any particular design elements for your website, or "
                "would you prefer elaa to select them according to your preferences?"
            ]

            # pick a random message
            message = random.choice(message_options)

            # save message as last_system_message when it is called
            state_manager.store_data('last_system_message', message)

            # set response type for user
            response_type = 'text'

            return {'message': message, 'response_type': response_type}
        else:
            # retrieve last_system_message
            last_system_message = state_manager.retrieve_data('last_system_message')

            # retrieve other information we would need
            website_name = state_manager.retrieve_data('website_name')
            portfolio_theme = state_manager.retrieve_data('portfolio_theme')
            professional_goals = state_manager.retrieve_data('professional_goals')
            template_type = state_manager.retrieve_data('template_type')

            # extract info from user input
            prompt_extraction = (
                f"Given the question {last_system_message} and user's answer is {user_input}."
                f"generate comprehensive design elements in JSON format. These elements should include color schemes,"
                f" fonts, spacing, breakpoints, animations, gradients, imagery style, interactive elements, "
                f"navigation style, content layout, and grid system. Ensure that the design suggestions are coherent"
                f" and align with modern web design principles, enhancing user experience and engagement. Ensure that "
                f"when deciding the design elements, pay specific attention to {user_input} and their related "
                f"information such as {website_name}, {portfolio_theme} and {professional_goals} ")

            get_design_scheme = text_bot.extraction(prompt_extraction)
            print(f"prompt_extraction: {get_design_scheme}")  # debug

            # save the input
            state_manager.store_data('design_elements', get_design_scheme)
            return self.final_interaction(state_manager)

    def final_interaction(self, state_manager):
        # Reset current step to None indicating the end of this node's process
        state_manager.set_current_step(None)

        # Final message to the user after gathering all the information
        message = "Thank you for providing these information. Give us a moment while we customise your template"
        response_type = None
        auto_progress = True
        next_node = 'CustomizeTemplate'

        return {'message': message, 'response_type': response_type, 'next_node': next_node,
                'auto_progress': auto_progress}


class CustomizeTemplate(Node):
    def __init__(self, name, next_node=None, requires_input=False):
        super().__init__(name, next_node, requires_input)

    def process(self, state_manager, user_input=None):
        template_id = state_manager.retrieve_data('template_id')

        # Retrieve the page in the template
        page = Page.query.filter_by(template_id=template_id, page_name='Home').first()

        if page:
            page_name = 'Home'
            self.modify_template(state_manager, page_name, page)

        next_node = 'DetermineNextStep'
        auto_progress = True
        return {'next_node': next_node, 'auto_progress': auto_progress}

    def modify_template(self, state_manager, page_name, page):
        # Get the ai services I will be using
        template_bot = ServiceLocator.get_service('template_bot')
        socketio = ServiceLocator.get_service('socketio')

        # Get all the information i need
        website_name = state_manager.retrieve_data('website_name')
        product = state_manager.retrieve_data('product')
        business_goal = state_manager.retrieve_data('business_goal')
        design_elements = state_manager.retrieve_data('design_elements')
        template_id = state_manager.retrieve_data('template_id')

        # Get the page for modification
        original_html = page.html_content
        original_css = page.css_content

        modification_instructions_html = (f"Modify the {page_name} HTML template to incorporate the website's theme"
                                          f" around {website_name}, the products/services offered ({product}),"
                                          f" and the business goals ({business_goal}). Enhance the layout to reflect"
                                          f" the {design_elements} theme, using HTML5 semantic elements for a rich,"
                                          f" interactive user experience. Prepare the layout for dynamic CSS effects as"
                                          f" described in {design_elements}, with comments indicating where these "
                                          f"effects should be applied. Do not generate the CSS stylings too, as we have"
                                          f" a different file for it. Ensure the structure is optimized for both "
                                          f"aesthetics and functionality, adhering to web accessibility standards."

                                          )

        updated_html = template_bot.modify_html(original_html, modification_instructions_html)

        # Update the modified template in the database
        DBUtils.update_template_in_db(template_id, page.page_name, updated_html, 'html')
        print(f"updated_html: {updated_html}")  # Debug

        # Retrieve the metadata of the html webpage to give css AI context
        metadata = template_bot.get_metadata(updated_html)

        # Then do css
        modification_instructions_css = (f"Create a cohesive CSS stylesheet for {page_name} that embodies the"
                                         f" {design_elements} theme, with special attention to {metadata} instructions."
                                         f" Utilize modern CSS techniques to bring the design elements to life, "
                                         f"ensuring consistency across the website. Apply styles according to the"
                                         f" metadata guidelines, focusing on animations, gradients, and responsive"
                                         f" design features that enhance the visual appeal and user experience. Aim for"
                                         f" a balance between creativity and usability, ensuring the site remains"
                                         f" accessible and performs well across devices."
                                         )

        updated_css = template_bot.modify_css(original_css, modification_instructions_css)
        # Update the modified template in the database
        DBUtils.update_template_in_db(template_id, page.page_name, updated_css, 'css')
        print(f"updated_css: {updated_css}")  # Debug

        # Refresh iframe
        socketio.emit('refresh_iframe')

        return {'message': f"{page_name} updated successfully"}
