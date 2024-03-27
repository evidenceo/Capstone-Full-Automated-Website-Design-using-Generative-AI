import random
from classes import Node, ServiceLocator, DBUtils
from models import UserTemplatePage
from flask import json


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
        elif current_step == "get_event_theme":
            return self.get_event_theme(state_manager, user_input)
        elif current_step == "get_event_goals":
            return self.get_event_goals(state_manager, user_input)
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
            state_manager.set_current_step("get_event_theme")
            return self.process(state_manager)

    def get_event_theme(self, state_manager, user_input):
        # Get text_bot
        text_bot = ServiceLocator.get_service('text_bot')
        if user_input is None:
            message_options = [
                "What kind of event are you looking to host?",
                "What kind of event are you hoping to put together?",
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
                f"Given {last_system_message} and {user_input}. Extract the event the user is hosting from the "
                f"information and save in JSON format. Only output JSON format result without any additional"
                f"explanation or text.")
            get_event_theme = text_bot.extraction(prompt_extraction)
            print(f"prompt_extraction: {get_event_theme}")  # debug

            # save the input
            state_manager.store_data('event_theme', get_event_theme)
            state_manager.set_current_step("get_event_goals")
            return self.process(state_manager)

    def get_event_goals(self, state_manager, user_input):
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
            get_event_goals = text_bot.extraction(prompt_extraction)
            print(f"prompt_extraction: {get_event_goals}")  # debug

            # save the input
            state_manager.store_data('event_goals', get_event_goals)

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
            event_theme = state_manager.retrieve_data('event_theme')
            event_goals = state_manager.retrieve_data('event_goals')
            template_type = state_manager.retrieve_data('template_type')

            # extract info from user input
            prompt_extraction = (
                f"Given the question {last_system_message} and user's answer is {user_input}."
                f"generate comprehensive design elements in JSON format. These elements should include color schemes,"
                f" fonts, spacing, breakpoints, animations, gradients, imagery style, interactive elements, "
                f"navigation style, content layout, and grid system. Ensure that the design suggestions are coherent"
                f" and align with modern web design principles, enhancing user experience and engagement. Ensure that "
                f"when deciding the design elements, pay specific attention to {user_input} and their related "
                f"information such as {website_name}, {event_theme} and {event_goals} ")

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
        socketio = ServiceLocator.get_service('socketio')

        user_template_id = state_manager.retrieve_data('user_template_id')

        # Start event to show loading indicator
        socketio.emit('show_loading', {'message': 'Customizing your template...'}, namespace='/')

        # Retrieve every page in the template
        pages = UserTemplatePage.query.filter_by(user_template_id=user_template_id).all()

        for page in pages:
            if page.page_name == 'Home':
                page_name = 'Home'
                self.modify_template(state_manager, page_name, page)

        # Stop loading
        socketio.emit('hide_loading', {'message': 'Customization complete'}, namespace='/')

        next_node = 'DetermineNextStep'
        auto_progress = True
        return {'next_node': next_node, 'auto_progress': auto_progress}

    def modify_template(self, state_manager, page_name, page):
        # Get the ai services I will be using
        template_bot = ServiceLocator.get_service('template_bot')
        socketio = ServiceLocator.get_service('socketio')

        # Get all the information i need
        website_name = state_manager.retrieve_data('website_name')
        event_theme = state_manager.retrieve_data('event_theme')
        event_goals = state_manager.retrieve_data('event_goals')
        design_elements = state_manager.retrieve_data('design_elements')
        user_template_id = state_manager.retrieve_data('user_template_id')

        # Get the page for modification
        original_html = page.modified_html
        original_css = page.modified_css

        modification_instructions_html = (f"Modify the HTML template to incorporate the website's theme"
                                          f" around {website_name}, the type of event ({event_theme}),"
                                          f" and the event goals ({event_goals}). Enhance the layout to reflect"
                                          f" the {design_elements} theme, using HTML5 semantic elements for a rich,"
                                          f" interactive user experience. Prepare the layout for dynamic CSS effects as"
                                          f" described in {design_elements}, with comments indicating where these "
                                          f"effects should be applied. Do not generate the CSS stylings too, as we have"
                                          f" a different file for it. Ensure the structure is optimized for both "
                                          f"aesthetics and functionality, adhering to web accessibility standards."

                                          )

        updated_html = template_bot.modify_html(original_html, modification_instructions_html)

        # Update the modified template in the database
        DBUtils.update_template_in_db(user_template_id, page.page_name, updated_html, 'html')
        print(f"updated_html: {updated_html}")  # Debug

        # Retrieve the metadata of the html webpage to give css AI context
        metadata = template_bot.get_metadata(updated_html)

        # Then do css
        modification_instructions_css = (f"Modify the CSS stylesheet given for an event HTML page that embodies the"
                                         f" {design_elements} theme, with special attention to {metadata} instructions."
                                         f" Utilize modern CSS techniques to bring the design elements to life, "
                                         f"ensuring consistency across the website. Apply styles according to the"
                                         f" metadata guidelines, focusing on animations, gradients, and responsive"
                                         f" design features that enhance the visual appeal and user experience. Aim for"
                                         f" a balance between creativity and usability, ensuring the site remains"
                                         f" accessible and performs well across devices. Make sure styles are applied"
                                         f" to all classes in the stylesheet."
                                         )

        updated_css = template_bot.modify_css(original_css, modification_instructions_css)
        # Update the modified template in the database
        DBUtils.update_template_in_db(user_template_id, page.page_name, updated_css, 'css')
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
            message = ("In the next stage of the conversation, you would be allowed to further customize your template"
                       " twice before ending the conversation. If you are satisfied with the current"
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
                next_node = 'CustomizeTwice'
                auto_progress = True

                return {'next_node': next_node, 'auto_progress': auto_progress}
            elif user_input == 'end':
                message = ("Got it. The conversation will end here. Click on the 'Next' button at the bottom right to"
                           " customize the template further in the edit dashboard")
                response_type = None
                next_node = None

                return {'message': message, 'response_type': response_type, 'next_node': next_node}


class CustomizeTwice(Node):
    def __init__(self, name, next_node=None, requires_input=True):
        super().__init__(name, next_node, requires_input)

    def process(self, state_manager, user_input=None):
        # Determine the current step in the process
        current_step = state_manager.get_current_step()

        # Manage the flow of the conversation
        if current_step is None or current_step == "first_iteration":
            return self.first_iteration(state_manager, user_input)
        elif current_step == "second_iteration":
            return self.second_iteration(state_manager, user_input)
        else:
            return self.first_iteration(state_manager)

    def first_iteration(self, state_manager, user_input):
        state_manager.set_current_step('first_iteration')
        template_bot = ServiceLocator.get_service('template_bot')
        text_bot = ServiceLocator.get_service('text_bot')
        socketio = ServiceLocator.get_service('socketio')

        if user_input is None:
            message = f"What would you like to further customize in this page?"
            # set response type for user
            response_type = 'text'

            # reset step
            state_manager.set_current_step(None)

            return {'message': message, 'response_type': response_type}
        else:
            user_template_id = state_manager.retrieve_data('user_template_id')
            page_name = 'Home'

            # Start event to show loading indicator
            socketio.emit('show_loading', {'message': 'Customizing your template...'}, namespace='/')

            # Retrieve current page
            current_page = UserTemplatePage.query.filter_by(user_template_id=user_template_id,
                                                            page_name=page_name).first()
            page_html = current_page.modified_html
            page_css = current_page.modified_css

            # Extract task from user input
            prompt_extraction = (
                f"Given the user's request to modify the website, categorize the changes that should be applied to the "
                f"HTML structure and those that should be applied through CSS styling. Bear in mind that there is a "
                f"template already and you'd just be making modifications to it so try to organize the task to make "
                f"use of what is already in the template. Organize the tasks under two "
                f"categories: 'html_change_request' for changes in the HTML structure and "
                f"'css_change_request' for styling changes. Format the output as JSON with these two keys, providing"
                f" detailed instructions under each category based on the user's request."
                f"User request: {user_input}. Please generate the categorized tasks in JSON format. Do not provide any"
                f"explanations or additional text. Thank you. "
            )

            design_update_json = text_bot.extraction(prompt_extraction)
            print(design_update_json)  # Debug

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
                        f"Refine the HTML for this portfolio page by incorporating the following changes"
                        f" requested by the user: {design_update['html_change_request']}. "
                        f"Ensure these modifications blend seamlessly with the existing "
                        f"content and layout, maintaining the page's overall aesthetics and "
                        f"functionality. Focus on enhancing user engagement and accessibility "
                        f"with the new content."
                    )

                    updated_html = template_bot.modify_html(page_html, modification_instructions_html)
                    # Update the modified template in the database
                    DBUtils.update_template_in_db(user_template_id, page_name, updated_html, 'html')
                    print(f"updated_html: {updated_html}")  # Debug
                else:
                    print("No HTML changes requested. Skipping to CSS modifications.")

                # Then do css
                modification_instructions_css = (
                    f"Update the CSS for this portfolio page to implement the following style modifications"
                    f" as requested by the user: {design_update['css_change_request']}. "
                    f"Apply these changes in a way that enhances the visual appeal and user "
                    f"experience of the website while ensuring consistency with the existing "
                    f"design theme. Prioritize responsive design and accessibility in these "
                    f"updates."
                )

                updated_css = template_bot.modify_css(page_css, modification_instructions_css)
                # Update the modified template in the database
                DBUtils.update_template_in_db(user_template_id, page_name, updated_css, 'css')
                print(f"updated_css: {updated_css}")  # Debug

                # Refresh iframe
                socketio.emit('refresh_iframe')  # Finsh loading

                # Stop loading
                socketio.emit('hide_loading', {'message': 'Customization complete'}, namespace='/')

                state_manager.set_current_step("second_iteration")
                return self.process(state_manager)

            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")

    def second_iteration(self, state_manager, user_input):
        template_bot = ServiceLocator.get_service('template_bot')
        text_bot = ServiceLocator.get_service('text_bot')
        socketio = ServiceLocator.get_service('socketio')

        if user_input is None:
            message = f"What would you like to further customize in this page?"
            # set response type for user
            response_type = 'text'

            # reset step
            state_manager.set_current_step(None)

            return {'message': message, 'response_type': response_type}
        else:
            user_template_id = state_manager.retrieve_data('user_template_id')
            page_name = 'Home'

            # Start event to show loading indicator
            socketio.emit('show_loading', {'message': 'Customizing your template...'}, namespace='/')

            # Retrieve current page
            current_page = UserTemplatePage.query.filter_by(user_template_id=user_template_id,
                                                            page_name=page_name).first()
            page_html = current_page.modified_html
            page_css = current_page.modified_css

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
            print(design_update_json)  # Debug

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
                        f"Refine the HTML for this portfolio page by incorporating the following changes"
                        f" requested by the user: {design_update['html_change_request']}. "
                        f"Ensure these modifications blend seamlessly with the existing "
                        f"content and layout, maintaining the page's overall aesthetics and "
                        f"functionality. Focus on enhancing user engagement and accessibility "
                        f"with the new content."
                    )

                    updated_html = template_bot.modify_html(page_html, modification_instructions_html)
                    # Update the modified template in the database
                    DBUtils.update_template_in_db(user_template_id, page_name, updated_html, 'html')
                    print(f"updated_html: {updated_html}")  # Debug
                else:
                    print("No HTML changes requested. Skipping to CSS modifications.")

                # Then do css
                modification_instructions_css = (
                    f"Update the CSS for this portfolio page to implement the following style modifications"
                    f" as requested by the user: {design_update['css_change_request']}. "
                    f"Apply these changes in a way that enhances the visual appeal and user "
                    f"experience of the website while ensuring consistency with the existing "
                    f"design theme. Prioritize responsive design and accessibility in these "
                    f"updates."
                )

                updated_css = template_bot.modify_css(page_css, modification_instructions_css)
                # Update the modified template in the database
                DBUtils.update_template_in_db(user_template_id, page_name, updated_css, 'css')
                print(f"updated_css: {updated_css}")  # Debug

                # Refresh iframe
                socketio.emit('refresh_iframe')  # Finsh loading

                # Stop loading
                socketio.emit('hide_loading', {'message': 'Customization complete'}, namespace='/')

                state_manager.set_current_step("finalize_interaction")
                return self.process(state_manager)

            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")

    def finalize_interaction(self, state_manager):
        message = ("I have carried out the modifications you requested. The conversation will end here. Click on the"
                   " 'Next' button at the bottom right to customize this template in the dashboard.")
        response_type = None
        next_node = self.next_node
        auto_progress = True

        return {'message': message, 'response_type': response_type, 'next_node': next_node,
                'auto_progress': auto_progress}


class FinalMessage(Node):
    def __init__(self, name, next_node=None, requires_input=False):
        super().__init__(name, next_node, requires_input)

    def process(self, state_manager, user_input=None):
        message = "Elaa signing out!"
        response_type = None

        # This is the end of the interaction, so no next_node or auto_progress is needed
        return {'message': message, 'response_type': response_type}
