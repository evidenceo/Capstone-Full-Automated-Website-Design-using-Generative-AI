import random
from classes import Node, ServiceLocator, DBUtils
from models import db, Page
from flask import current_app


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

        if current_step is None or current_step == "get_website_name":
            # first get website name
            return self.get_website_name(state_manager, user_input)
        elif current_step == "get_product":
            return self.get_product(state_manager, user_input)
        elif current_step == "get_business_goal":
            return self.get_business_goal(state_manager, user_input)
        elif current_step == "get_colour_scheme":
            return self.colour_scheme(state_manager, user_input)
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
                "Please provide a name for your website."
            ]

            # pick a random message
            message = random.choice(message_options)

            # save message as last_system_message when it is called
            state_manager.store_data('last_system_message', message)

            # set response type for user
            response_type = 'text'

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
            state_manager.set_current_step("get_product")
            return self.process(state_manager)

    def get_product(self, state_manager, user_input):
        # Get text_bot
        text_bot = ServiceLocator.get_service('text_bot')
        if user_input is None:
            message_options = [
                "What products would you be selling on this website?",
                "What type of items do you plan to sell through this website?"
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
            get_product = text_bot.extraction(prompt_extraction)
            print(f"prompt_extraction: {get_product}")  # debug

            # save the input
            state_manager.store_data('product', get_product)
            state_manager.set_current_step("get_business_goal")
            return self.process(state_manager)

    def get_business_goal(self, state_manager, user_input):
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
            get_business_goal = text_bot.extraction(prompt_extraction)
            print(f"prompt_extraction: {get_business_goal}")  # debug

            # save the input
            state_manager.store_data('business_goal', get_business_goal)

            state_manager.set_current_step("get_colour_scheme")
            return self.process(state_manager)

    def colour_scheme(self, state_manager, user_input):
        # Get text_bot
        text_bot = ServiceLocator.get_service('text_bot')
        if user_input is None:
            message_options = [
                "Almost there!\n If you already have specific colors in mind for your website, please feel free to "
                "provide them. Otherwise, would you like elaa to suggest a color scheme based on your preferences?",

                "Final Round!\nFeel free to share any preferred colors you have in mind for your website. "
                "Alternatively, would you like elaa to propose a color scheme based on your preferences?"
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
            product = state_manager.retrieve_data('product')
            business_goal = state_manager.retrieve_data('business_goal')
            template_type = state_manager.retrieve_data('template_type')

            # extract info from user input
            prompt_extraction = (
                f"Given {last_system_message} and {user_input}, use the provided user information "
                f"(website name:{website_name}, product:{product}, business goal:{business_goal} and "
                f"template type:{template_type}) to generate a comprehensive color scheme for the website. "
                f"Populate the following color categories based on context: primary colors, secondary colors, "
                f"background colors, text colors, accent colors, border colors, error colors, neutral colors, and "
                f"hover/focus colors. Save the generated color scheme in JSON format.If the user does not provide any "
                f"color preferences, use the provided context to generate a suitable color scheme. Only output JSON "
                f"format result without any additional explanation or text.")

            get_colour_scheme = text_bot.extraction(prompt_extraction)
            print(f"prompt_extraction: {get_colour_scheme}")  # debug

            # save the input
            state_manager.store_data('colour_scheme', get_colour_scheme)
            return self.finalize_interaction(state_manager)

    def finalize_interaction(self, state_manager):
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

        # Retrieve every page in the template
        pages = Page.query.filter_by(template_id=template_id).all()

        for page in pages:
            if page.page_name == 'Home':
                page_name = 'Home'
                self.modify_template(state_manager, page_name, page)
            elif page.page_name == 'About':
                page_name = 'About'
                self.modify_template(state_manager, page_name, page)
            elif page.page_name == 'Products':
                page_name = 'Products'
                self.modify_template(state_manager, page_name, page)
            elif page.page_name == 'Contact':
                page_name = 'Contact'
                self.modify_template(state_manager, page_name, page)

        next_node = 'DetermineNextStep'
        auto_progress = True
        return {'next_node': next_node, 'auto_progress': auto_progress}

    def modify_template(self, state_manager, page_name, page):
        template_bot = ServiceLocator.get_service('template_bot')
        socketio = ServiceLocator.get_service('socketio')

        # Get all the information i need
        website_name = state_manager.retrieve_data('website_name')
        product = state_manager.retrieve_data('product')
        business_goal = state_manager.retrieve_data('business_goal')
        colour_scheme = state_manager.retrieve_data('colour_scheme')
        template_id = state_manager.retrieve_data('template_id')

        original_html = page.html_content
        original_css = page.css_content

        modification_instructions_html = (f"Given the following information: {website_name}, {product} and"
                                          f" {business_goal}, tailor the {page_name} html page, {original_html} to these"
                                          f" information.")

        updated_html = template_bot.modify_html(original_html, modification_instructions_html)
        # Update the modified template in the database
        DBUtils.update_template_in_db(template_id, page.page_name, updated_html, 'html')
        print(f"updated_html: {updated_html}")  # Debug

        # Then do css
        modification_instructions_css = (f"Tailor {page_name} css page to this colour scheme: {colour_scheme} and "
                                         f"modify font to fit the characteristics of {product} "
                                         f"and {business_goal}")

        updated_css = template_bot.modify_css(original_css, modification_instructions_css)
        # Update the modified template in the database
        DBUtils.update_template_in_db(template_id, page.page_name, updated_css, 'css')
        print(f"updated_css: {updated_css}")  # Debug

        # Refresh iframe
        socketio.emit('refresh_iframe')

        return {'message': f"{page_name} updated successfully"}


class DetermineNextStep(Node):
    def __init__(self, name, next_node=None, skip_node=None,requires_input=False):
        super().__init__(name, next_node, requires_input)
        self.skip_node = skip_node

    def process(self, state_manager, user_input=None):
        print("Here right now") # For debug - it prints
        action = 'show_popup'
        message = ("The next part of the conversation involves customizing each page to further meet your goals. If you"
                   "are okay with the current customization, you can skip this step, otherwise let's continue")
        buttons = [
            {'label': 'Continue', 'value': 'continue'},
            {'label': 'Skip', 'value': 'skip'}
        ]
        next_node = None
        return {
            'action': action,
            'message': message,
            'buttons' : buttons,
            'next_node': next_node
        }
        # Here I want a popup first that blurs the background with a message that says
        # Hi Elaa here! The next step is to further customize your template in this stage we would iterate each page
        # and customize the structure to meet your preferences. If you are okay with the structure at the moment,
        # skip this step and move to the design board, otherwise click continue

        # Then there would be two buttons [continue] and [skip]

        # Work on [continue] now. when the user clicks on continue, it would go back and continue the conversation in
        # the chatbot starting with home page