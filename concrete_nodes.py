import random
from classes import Node, ServiceLocator, DBUtils
from models import db, Page


# Implement specific conversation steps by extending 'Node' class

class WelcomeNode(Node):
    def __init__(self, name, next_node=None):
        super().__init__(name, next_node)

    def process(self, state_manager, user_input=None):
        message = "Welcome to Elaa, your AI web designer! Let's start creating your dream website."
        next_node = "GetWebsiteName"
        response_type = 'text'
        auto_progress = True
        return {'message': message, 'response_type': response_type, 'next_node': next_node,
                'auto_progress': auto_progress}


class GetWebsiteName(Node):
    def __init__(self, name, next_node=None):
        super().__init__(name, next_node)

    def process(self, state_manager, user_input=None):
        socketio = ServiceLocator.get_service('socketio')
        template_bot = ServiceLocator.get_service('template_bot')

        if not user_input:
            # First send the message to user
            message = "What would you like to name your website?"
            response_type = "text"
            return {'message': message, 'response_type': response_type}
        else:
            # Save user input as website name
            state_manager.store_data('website_name', user_input)

            # Retrieve current template
            template_id = state_manager.retrieve_data('template_id')
            print(template_id)  # Debug

            # Fetch all pages for the current template from the database
            pages = Page.query.filter_by(template_id=template_id).all()

            # Retrieve and modify every html page from the database
            for page in pages:
                original_html = page.html_content
                print(f"currenthtml: {original_html}")  # Debug

                # Modify the HTML template using AI with the website name
                modification_instructions = f"replace (website_name) with {user_input}"
                updated_template = template_bot.modify_html(original_html, modification_instructions)

                # Update the modified template in the database
                DBUtils.update_template_in_db(template_id, page.page_name, updated_template, 'html')
                print(f"updatedhtml: {updated_template}")  # Debug

                # Emit the modified template to the client to update the iframe
                socketio.emit('update_template', {'template': updated_template})

            # Now move to the next node
            next_node = "GetBusinessGoal"
            response_type = None
            auto_progress = True
            return {'response_type': response_type, 'next_node': next_node,
                    'auto_progress': auto_progress}


class GetBusinessGoal(Node):
    def __init__(self, name, next_node=None):
        super().__init__(name, next_node)

    def process(self, state_manager, user_input=None):
        text_bot = ServiceLocator.get_service('text_bot')

        # First get user input
        if not user_input:
            prompt_dynamic = "In a short and simple sentence, ask the user of their business goal or product they sell."
            message = text_bot.dynamic_message(prompt_dynamic)
            response_type = 'text'

            # Save message to be used later
            state_manager.store_data('last_system_message', message)

            return {'message': message, 'response_type': response_type}
        else:
            # Extract information from user's input
            last_system_message = state_manager.retrieve_data('last_system_message')
            print(f"last_system_message:{last_system_message}")  # Debug

            prompt_extraction = (
                f"Giving the following information: {last_system_message} and {user_input},extract the "
                f"users business goal or product that they sell and store it json format.")
            business_goal = text_bot.extraction(prompt_extraction)
            print(f"businessgoal: {business_goal}")  # Debug

            # Save it to be use later
            state_manager.store_data('business_goal', business_goal)

            # Finally send message to user
            message_options = ["Now let's talk branding...", "Great! Now let's shift our focus to branding..."]

            # pick a random message to send to user and move to next node
            message = random.choice(message_options)
            next_node = "GetWebsiteTheme"
            response_type = None
            auto_progress = True

            return {'message': message, 'response_type': response_type, 'next_node': next_node,
                    'auto_progress': auto_progress}


class GetWebsiteTheme(Node):
    def __init__(self, name, next_node=None):
        super().__init__(name, next_node)

    def process(self, state_manager, user_input=None):
        text_bot = ServiceLocator.get_service('text_bot')
        template_bot = ServiceLocator.get_service('template_bot')
        socketio = ServiceLocator.get_service('socketio')

        if not user_input:
            # First send input message
            message_options = ["We want to make this template feel all you. Are there any specific colors, fonts or "
                               "design"
                               " elements that represent your brand or would you like some suggestions?",
                               "Let's give this template your personal touch. Do you have any colors, fonts or design "
                               "elements that embody your brand, or would you appreciate some suggestions?",
                               "Our goal is to tailor this template to reflect your brand essence. Are there any "
                               "specific"
                               "colors, fonts, or design elements that resonate with your brand, or are you open to "
                               "exploring some suggestions?"]

            # pick a random message to send
            message = random.choice(message_options)
            # save last system response
            state_manager.store_data('last_system_message', message)

            response_type = 'button'

            # Define the buttons you want to send
            buttons = [
                {'name': 'Use Brand theme', 'value': 'brand_theme'},
                {'name': 'Get Suggestions', 'value': 'suggestions'}
            ]

            return {'message': message, 'response_type': response_type, 'buttons': buttons}

            # now you have user input determine the next step
        elif user_input == 'brand_theme':
            # save user_input
            state_manager.store_data('design_path', user_input)
            print(f"user_input: {user_input}")  # Debug

            # Ask the user for the following information
            message = ("How can we incorporate your branding elements into the template? Please provide the color "
                       "scheme, font and any other design elements specific to your brand.")
            response_type = 'text'
            next_node = 'SetWebsiteTheme'

            # store last_system_message
            state_manager.store_data('last_system_message', message)

            state_manager.store_data('last_user_message', 'user_input')

            return {'message': message, 'response_type': response_type, 'next_node': next_node}

        elif user_input == 'suggestions':
            # save user_input
            state_manager.store_data('design_path', user_input)

            # First get the information that we'll need
            website_name = state_manager.retrieve_data('website_name')
            business_goal = state_manager.retrieve_data('business_goal')
            template_type = state_manager.retrieve_data('template_type')

            # Prompt the ai to generate suggestions for user
            prompt_dynamic = (f"Given the following information: {template_type}, {business_goal} and {website_name}, "
                              f"generate three simple design suggestions on color, font and design elements, that can"
                              f" be implemented with css only for the user. Begin your response with"
                              f" 'Here are three design suggestions:...'  and end with a question asking the user which of"
                              f" the suggestions they's like to go with.")
            message = text_bot.dynamic_message(prompt_dynamic)
            print(f"message: {message}")  # Debug

            # save the suggestions
            state_manager.store_data('design_suggestions', message)

            state_manager.store_data('last_user_message', 'user_input')

            response_type = 'text'
            next_node = 'SetWebsiteTheme'

            return {'message': message, 'response_type': response_type, 'next_node': next_node}


class SetWebsiteTheme(Node):
    def __init__(self, name, next_node=None):
        super().__init__(name, next_node)

    def process(self, state_manager, user_input=None):
        text_bot = ServiceLocator.get_service('text_bot')

        # Retrieve design path
        design_path = state_manager.retrieve_data('design_path')

        if design_path == 'brand_theme':

            if state_manager.retrieve_data('last_user_message') == 'user_input':
                state_manager.store_data('last_user_message', user_input)

            # Retrieve last_user_message and last_system_message
            last_user_message = state_manager.retrieve_data('last_user_message')
            last_system_message = state_manager.retrieve_data('last_system_message')

            prompt_extraction = (f"Given this question {last_system_message} and answer {last_user_message}. Check if "
                                 f"you can extract the following information from the answer: Brand color, Font, Design"
                                 f" elements. For any information that falls within any of the categories, extract them"
                                 f" and store it in json format.")

            design = text_bot.extraction(prompt_extraction)

            # Store this information
            state_manager.store_data('design_elements', design)

            # Retrieve information
            design_elements = state_manager.retrieve_data('design_elements')

            self.update_css(state_manager, design_elements)

        elif design_path == 'suggestion':

            if state_manager.retrieve_data('last_user_message') == 'user_input':
                state_manager.store_data('last_user_message', user_input)

            # Retrieve last_user_message and design_suggestions
            last_user_message = state_manager.retrieve_data('last_user_message')
            design_suggestion = state_manager.retrieve_data('design_suggestions')

            # prompt ai to extract users chosen suggestions
            prompt_extraction = (f"Given the system message {design_suggestion}, the user gave this reply: {last_user_message},"
                                 f"Determine the chosen suggestion, classify it into three categories: Brand color "
                                 f"scheme, Font and Design elements. Save the information in json format.")

            design = text_bot.extraction(prompt_extraction)

            # Store this information
            state_manager.store_data('design_elements', design)

            # Retrieve information
            design_elements = state_manager.retrieve_data('design_elements')

            # Modify the template
            self.update_css(design_elements)

    def update_css(self, state_manager, design_elements):
        template_bot = ServiceLocator.get_service('template_bot')
        socketio = ServiceLocator.get_service('socketio')

        # Retrieve current template
        template_id = state_manager.retrieve_data('template_id')

        # Fetch all pages for the current template from the database
        page = Page.query.filter_by(template_id=template_id, page_name='Home').first()

        # Fetch one css content
        if page:
            original_css = page.css_content
            print(f"original_css: {original_css}") # Debug

        # Now modify the css
        modification_instructions = (f"Modify the following classes using this information: {design_elements}."
                                     f" Do not add or remove any class, just modify the ones given.")

        updated_css = template_bot.modify_css(original_css, modification_instructions)
        print(f"updatedcss:{updated_css}") # Debug

        # Since the css in all of them is the same at this point, we will just modify one and update the rest
        # with it

        # Now get all the pages' css
        pages = Page.query.filter_by(template_id=template_id).all()

        # The update all of them
        for page in pages:
            DBUtils.update_template_in_db(template_id, page.page_name, updated_css, 'css')

        # After updating the CSS content in the database
        socketio.emit('refresh_iframe')

        return {'message': "css updated successfully"}




       




