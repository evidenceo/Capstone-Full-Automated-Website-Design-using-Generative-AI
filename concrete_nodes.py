import json
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
        self.skip_node = "HomePage"

    def process(self, state_manager, user_input=None):
        # Determine the current step in the process
        current_step = state_manager.get_current_step()

        # manage the flow of thw conversation
        if current_step is None or current_step == "get_website_name":
            # first get website name
            return self.get_website_name(state_manager, user_input)
        elif current_step == "get_product":
            return self.get_product(state_manager, user_input)
        elif current_step == "get_business_goal":
            return self.get_business_goal(state_manager, user_input)
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
                "Please provide a name for your website."
            ]

            # pick a random message
            message = random.choice(message_options)

            # save message as last_system_message when it is called
            state_manager.store_data('last_system_message', message)

            # set response type for user
            response_type = 'hybrid' # allows for both text and button

            # Button for user to skip this step
            button = [{'name': 'Skip to Page modification', 'value': 'skip'}]

            return {'message': message, 'response_type': response_type, 'button': button}
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

            state_manager.set_current_step("get_design_elements")
            return self.process(state_manager)

    def design_elements(self, state_manager, user_input):
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
                f"Given the question {last_system_message} and user's answer is {user_input}."
                f"generate comprehensive design elements in JSON format. These elements should include color schemes,"
                f" fonts, spacing, breakpoints, animations, gradients, imagery style, interactive elements, "
                f"navigation style, content layout, and grid system. Ensure that the design suggestions are coherent"
                f" and align with modern web design principles, enhancing user experience and engagement. Ensure that "
                f"when deciding the design elements, pay specific attention to {user_input} and their related "
                f"information such as {website_name}, {product} and {business_goal} ")

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


class DetermineNextStep(Node):
    def __init__(self, name, next_node=None, requires_input=True):
        super().__init__(name, next_node, requires_input)

    def process(self, state_manager, user_input=None):
        if user_input is None:
            # send message to frontend to show the damn popup
            action = 'show_popup'
            message = ("In the next stage of the conversation, we would be going through each website page in the"
                       " template to further customize it to your preferences. If you are satisfied with the current"
                       " implementation, You can end the conversation, otherwise click on the 'Continue' button to"
                       " continue this conversation.")
            buttons = [
                {'name': 'Continue', 'value': 'continue'},
                {'name': 'End', 'value': 'end'}
            ]
            response_type = 'button'

            return {'action': action, 'message': message, 'buttons': buttons, 'response_type': response_type}
        else:
            if user_input == 'continue':
                next_node = 'HomePage'
                auto_progress = True

                return {'next_node': next_node, 'auto_progress': auto_progress}
            elif user_input == 'end':
                message = ("Got it. The conversation will end here. Click on the 'Next' button at the bottom right to"
                           " customize the template further in the edit dashboard")
                response_type = None
                next_node = None

                return {'message': message, 'response_type': response_type, 'next_node': next_node}


class BasePageModification(Node):
    def __init__(self, name, page_name, next_node=None, requires_input=True):
        super().__init__(name, next_node, requires_input)
        self.page_name = page_name # Specific page to be modified

    def process(self, state_manager, user_input=None):
        current_step = state_manager.get_current_step()

        if current_step is None or current_step == 'request_changes':
            return self.request_changes(state_manager, user_input)
        elif current_step == 'finalize_interaction':
            return self.finalize_interaction(state_manager)

    def request_changes(self, state_manager, user_input):
        state_manager.set_current_step('request_changes')
        template_bot = ServiceLocator.get_service('template_bot')
        text_bot = ServiceLocator.get_service('text_bot')
        socketio = ServiceLocator.get_service('socketio')

        if user_input is None:
            message = f"What would you like to change in the {self.page_name} page?"
            response_type = "text"
            return {'message': message, 'response_type': response_type}
        else:
            template_id = state_manager.retrieve_data('template_id')
            page_name = self.page_name

            # Retrieve current page
            current_page = Page.query.filter_by(template_id=template_id, page_name=page_name).first()
            page_html = current_page.html_content
            page_css = current_page.css_content

            # Extract task from user input
            prompt_extraction = (
                f"Given the user's request to modify the website, categorize the changes that should be applied to the "
                f"HTML structure and those that should be applied through CSS styling. Organize the tasks under two "
                f"categories: 'html_change_request' for changes in the HTML structure and "
                f"'css_change_request' for styling changes. Format the output as JSON with these two keys, providing"
                f" detailed instructions under each category based on the user's request."
                f"User request: {user_input}. Please generate the categorized tasks in JSON format."
            )

            design_update_json = text_bot.extraction(prompt_extraction)
            print(design_update_json) # Debug

            # Remove Markdown code block syntax if present
            if design_update_json.startswith("```json") and design_update_json.endswith("```"):
                # Strip off the Markdown code block delimeters
                design_update_json = design_update_json[7:-3].strip()

            try:
                # Then start modification
                """Loading Frontend - Begin"""
                design_update = json.loads(design_update_json)
                print(f"Design update tasks: {design_update}")  # debug

                # Check if HTML changes are requested
                if design_update.get("html_change_request"):
                    # If the list is not empty, process HTML changes
                    modification_instructions_html = (
                        f"Refine the HTML for {page_name} by incorporating the following changes"
                        f" requested by the user: {design_update['html_change_request']}. "
                        f"Ensure these modifications blend seamlessly with the existing "
                        f"content and layout, maintaining the page's overall aesthetics and "
                        f"functionality. Focus on enhancing user engagement and accessibility "
                        f"with the new content."
                    )

                    updated_html = template_bot.modify_html(page_html, modification_instructions_html)
                    # Update the modified template in the database
                    DBUtils.update_template_in_db(template_id, page_name, updated_html, 'html')
                    print(f"updated_html: {updated_html}")  # Debug
                else:
                    print("No HTML changes requested. Skipping to CSS modifications.")

                # Then do css
                modification_instructions_css = (
                    f"Update the CSS for {page_name} to implement the following style modifications"
                    f" as requested by the user: {design_update['css_change_request']}. "
                    f"Apply these changes in a way that enhances the visual appeal and user "
                    f"experience of the website while ensuring consistency with the existing "
                    f"design theme. Prioritize responsive design and accessibility in these "
                    f"updates."
                )

                updated_css = template_bot.modify_css(page_css, modification_instructions_css)
                # Update the modified template in the database
                DBUtils.update_template_in_db(template_id, page_name, updated_css, 'css')
                print(f"updated_css: {updated_css}")  # Debug

                # Refresh iframe
                socketio.emit('refresh_iframe')  # Finsh loading

                state_manager.set_current_step("finalize_interaction")
                return self.process(state_manager)

            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")

    def finalize_interaction(self, state_manager):
        message = "Changes have been made. Let us move to the next page."
        response_type = None
        next_node = self.next_node
        auto_progress = True

        # reset step
        state_manager.set_current_step(None)

        return {'message': message, 'response_type': response_type, 'next_node': next_node,
                'auto_progress': auto_progress}



# Now use this BaseClass for all the pages

class HomePage(BasePageModification):
    def __init__(self, name, next_node='AboutPage', requires_input=True):
        super().__init__(name, page_name='Home', next_node=next_node, requires_input=requires_input)


class AboutPage(BasePageModification):
    def __init__(self, name, next_node='ProductPage', requires_input=True):
        super().__init__(name, page_name='About', next_node=next_node, requires_input=requires_input)


class ProductPage(BasePageModification):
    def __init__(self, name, next_node='ContactPage', requires_input=True):
        super().__init__(name, page_name='Products', next_node=next_node, requires_input=requires_input)


class ContactPage(BasePageModification):
    def __init__(self, name, next_node='FinalMessage', requires_input=False):
        super().__init__(name, page_name='Contact', next_node=next_node, requires_input=requires_input)

    def finalize_interaction(self, state_manager):
        message = ("I have carried out the modifications you requested. The conversation will end here. Click on the"
                   " 'Next' button at the bottom right to customize this template in the dashboard.")
        response_type = None
        next_node = self.next_node
        auto_progress = True

        return {'message': message, 'response_type': response_type, 'next_node': next_node, 'auto_progress': auto_progress}


class FinalMessage(Node):
    def __init__(self, name, next_node=None, requires_input=False):
        super().__init__(name, next_node, requires_input)

    def process(self, state_manager, user_input=None):
        message = "Elaa signing out!"
        response_type = None

        # This is the end of the interaction, so no next_node or auto_progress is needed
        return {'message': message, 'response_type': response_type}


