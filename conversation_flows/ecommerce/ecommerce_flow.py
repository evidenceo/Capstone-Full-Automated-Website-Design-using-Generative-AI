import json
import random
from classes import Node, ServiceLocator, DBUtils
from models import UserTemplatePage


# Implement specific conversation steps by extending 'Node' class

class WelcomeNode(Node):
    def __init__(self, name, next_node=None, requires_input=False):
        super().__init__(name, next_node, requires_input)

    def process(self, state_manager, user_input=None):
        message_options = [
            "Welcome to Elaa, your AI web designer! Let's begin.",
            "Hello! I'm Elaa, your personal AI web designer. Let's get started on crafting your dream website."
        ]
        # pick a random message
        message = random.choice(message_options)
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

        # manage the flow of the conversation
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
            response_type = 'hybrid'  # allows for both text and button

            # Button for user to skip this step
            buttons = [{'name': 'Skip to Page modification', 'value': 'skip'}]

            # reset step
            state_manager.set_current_step(None)

            return {'message': message, 'response_type': response_type, 'buttons': buttons}
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
                "Awesome! What do goals do you have for this website?",
                "Awesome! What are the main goals you're looking to achieve with your website?"
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
                "Almost there!\n Do you have any specific design elements in mind for your website? Or would you like"
                " Elaa to choose them based on your preferences?",

                "We're nearly finished! Would you like to suggest any particular design elements for your website, or "
                "would you prefer Elaa to select them according to your preferences?"
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

            # extract info from user input
            prompt_extraction = (f"Generate a web design blueprint in JSON format for modifying an existing website"
                                 f" template composed of HTML and CSS. The blueprint should encompass key design "
                                 f"elements essential for a cohesive, user-centric web experience. Utilize the provided"
                                 f" information to tailor the blueprint, ensuring it aligns with the specific needs and"
                                 f" goals of the website. The blueprint must include detailed specifications for the "
                                 f"following elements:"
                                 f"- Website Name: {website_name}"
                                 f"- Product: {product}"
                                 f"- Business Goal: {business_goal}"
                                 f"- Color Scheme: Suggest based on {product}, {business_goal}, and {user_input} "
                                 f"(if specified)"
                                 f"- Typography: Recommend font styles and usage for consistency and readability"
                                 f"- Interactive Elements: Detail the design for buttons, forms, and other interactive"
                                 f" components"
                                 f"- Imagery and Visual Elements: Outline the approach for using images, icons, and "
                                 f"graphics"
                                 f"- Responsive Design and Breakpoints: Define how the website will adapt to different "
                                 f"screen sizes for optimal user experience"
                                 f"Consider the user's response regarding preferred design elements ({user_input}) to "
                                 f"guide your recommendations, especially for color scheme and typography choices. The "
                                 f"goal is to create a blueprint that reflects the website’s identity, enhances the "
                                 f"presentation of {product}, and supports the achievement of {business_goal}."
                                 f"Please output the result in JSON format, focusing solely on the design blueprint.")

            get_design_blueprint = text_bot.extraction(prompt_extraction)
            print(f"prompt_extraction: {get_design_blueprint}")  # debug

            # save the input
            state_manager.store_data('design_blueprint', get_design_blueprint)
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
            elif page.page_name == 'About':
                page_name = 'About'
                self.modify_template(state_manager, page_name, page)
            elif page.page_name == 'Product':
                page_name = 'Product'
                self.modify_template(state_manager, page_name, page)
            elif page.page_name == 'Contact':
                page_name = 'Contact'
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
        design_blueprint = state_manager.retrieve_data('design_blueprint')
        user_template_id = state_manager.retrieve_data('user_template_id')

        # Get the page for modification
        original_html = page.modified_html
        original_css = page.modified_css

        modification_instructions_html = (f"Given the design blueprint {design_blueprint}, meticulously modify the"
                                          f" provided HTML code to align with the blueprint's specifications. The "
                                          f"objective is to structure the HTML in a way that seamlessly integrates "
                                          f"with the CSS stylings outlined in the blueprint. To achieve this, pay "
                                          f"close attention to the following guidelines:"
                                          f"1. Apply HTML5 semantic elements (such as <header>, <footer>, <section>, "
                                          f"and <article>) to improve the structure and accessibility of the web "
                                          f"content, ensuring it matches the layout and sectioning detailed in the "
                                          f"blueprint."
                                          f"2. Where the design blueprint specifies styles for specific sections, "
                                          f"elements, or components but lacks corresponding classes or IDs, introduce"
                                          f" appropriate class or ID attributes. Choose meaningful names that reflect"
                                          f" the content or function of the element (e.g., 'product-list', "
                                          f"'contact-form'). 3. For interactive elements detailed in the blueprint, "
                                          f"such as buttons or forms, ensure they are implemented with HTML5 "
                                          f"attributes that enhance usability and accessibility. For example, "
                                          f"use <button> elements for actions and ensure <form> elements have proper"
                                          f" labeling. 4. Incorporate placeholders for imagery and visual elements "
                                          f"as specified in the blueprint. Use <img> tags with 'alt' attributes for "
                                          f"images, and consider placeholders for any icons or graphics, ensuring they "
                                          f"can be easily targeted with CSS for styling. 5. Ensure the document is "
                                          f"structured to facilitate responsive design, with a clear hierarchy and "
                                          f"layout that adapts based on the breakpoints defined in the blueprint. "
                                          f"This may involve organizing content within container elements that can be "
                                          f"dynamically styled using CSS. Remember, the aim is to refine the HTML "
                                          f"code so it not only embodies the aesthetic and functional aspirations of "
                                          f"the design blueprint but also lays a solid foundation for the subsequent "
                                          f"CSS enhancements. Please provide the modified HTML code, enhanced "
                                          f"according to these instructions, using HTML5 standards.")

        updated_html = template_bot.modify_html(original_html, modification_instructions_html)

        # Update the modified template in the database
        DBUtils.update_template_in_db(user_template_id, page.page_name, updated_html, 'html')
        print(f"updated_html: {updated_html}")  # Debug

        # Retrieve the metadata of the html webpage to give css AI context
        metadata = template_bot.get_metadata(updated_html)

        # Then do css
        modification_instructions_css = (f"Given the newly modified HTML structure: {metadata} appropriate class and ID"
                                         f" attributes for styling, and placeholders for interactive and visual elements"
                                         f" as outlined in the {design_blueprint}, create CSS stylings that bring the "
                                         f"design blueprint to life. Follow these key directives: "
                                         f"1. Color Scheme: Implement the color scheme specified in the design blueprint"
                                         f" across all elements, ensuring a harmonious and visually appealing interface."
                                         f" Apply primary, secondary, accent, background, and text colors to appropriate"
                                         f" elements, matching their identifiers in the updated HTML. "
                                         f"2. Typography: Style textual content using the font families, sizes, and "
                                         f"weights outlined in the blueprint. Ensure that headings, paragraphs, buttons,"
                                         f" and navigation items reflect the specified typography settings, enhancing "
                                         f"readability and aesthetic appeal. "
                                         f"3. Layout and Grid System: Utilize the grid system from the blueprint to "
                                         f"structure the page layouts. Apply CSS Grid or Flexbox to organize content "
                                         f"according to the specified columns, margins, and gutters, ensuring "
                                         f"responsive and adaptive design across different devices and screen sizes. "
                                         f"4. Interactive Elements: Style buttons, forms, and other interactive "
                                         f"components according to the interactive elements guide in the blueprint. "
                                         f"Focus on hover states, animations, and other dynamic effects that encourage"
                                         f" user interaction, using classes and IDs to target these elements specifically."
                                         f"5. Imagery and Visual Styling: Apply CSS to style imagery, icons, and "
                                         f"graphics as per the blueprint. This includes setting sizes, adding overlays "
                                         f"or filters, and positioning visual elements to complement the content layout."
                                         f"6. Responsive Design: Implement responsive design features using media "
                                         f"queries based on the breakpoints defined in the blueprint. Ensure that the "
                                         f"website's layout, typography, and interactive elements adjust smoothly across"
                                         f" different devices.The goal is to produce a cohesive CSS stylesheet that "
                                         f"accurately applies the design blueprint's aesthetic and functional "
                                         f"specifications to the updated HTML code. This CSS should enhance user "
                                         f"experience, emphasize the product or service offered, and support the "
                                         f"website's business goals. Please output the CSS code modifications "
                                         f"necessary to achieve this.")

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
            message = ("Next, we'll customize each page of the template to your preferences. If you're happy with the"
                       "current setup, feel free to end the conversation. Otherwise, click 'Continue' to proceed.")
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
                           " customize the template further in the Edit Dashboard")
                response_type = None
                next_node = None

                return {'message': message, 'response_type': response_type, 'next_node': next_node}


class BasePageModification(Node):
    def __init__(self, name, page_name, next_node=None, requires_input=True):
        super().__init__(name, next_node, requires_input)
        self.page_name = page_name  # Specific page to be modified

    def process(self, state_manager, user_input=None):
        current_step = state_manager.get_current_step()

        if current_step is None or current_step == 'request_changes':
            return self.request_changes(state_manager, user_input)
        elif current_step == 'finalize_interaction':
            return self.finalize_interaction(state_manager)
        return {}

    def request_changes(self, state_manager, user_input):
        state_manager.set_current_step('request_changes')
        template_bot = ServiceLocator.get_service('template_bot')
        text_bot = ServiceLocator.get_service('text_bot')
        socketio = ServiceLocator.get_service('socketio')

        if user_input is None:
            message_options =[
                "What specific changes would you like on this page?",
                f"What would you like to change in the {self.page_name} page? "
            ]
            message = random.choice(message_options)

            # set response type for user
            response_type = 'hybrid'  # allows for both text and button

            # Button for user to skip this step
            buttons = [{'name': 'Skip to Next Page', 'value': 'skip'}]

            # reset step
            state_manager.set_current_step(None)

            return {'message': message, 'response_type': response_type, 'buttons': buttons}
        else:
            user_template_id = state_manager.retrieve_data('user_template_id')
            page_name = self.page_name

            # Start event to show loading indicator
            socketio.emit('show_loading', {'message': 'Customizing your template...'}, namespace='/')

            # Retrieve current page
            current_page = UserTemplatePage.query.filter_by(user_template_id=user_template_id,
                                                            page_name=page_name).first()
            page_html = current_page.modified_html
            page_css = current_page.modified_css

            # Extract task from user input
            prompt_extraction = (
                f"Based on the user's feedback for selected website page, extract the specific modifications required."
                f"User feedback: '{user_input}'. Identify the key elements needing changes, such as colors, text content"
                f"layout adjustments, or any specified preferences."
            )

            extracted_modifications = text_bot.extraction(prompt_extraction)

            modification_instructions_html = (
                f"Given the extracted modifications: {extracted_modifications}, revise the HTML code to incorporate "
                f"these changes. Ensure the modifications allow for CSS styling, including adding necessary classes or"
                f"IDs for sections requiring style adjustments. Maintain HTML5 standards for enhanced accessiility and"
                f"web practices."
            )

            updated_html = template_bot.modify_html(page_html, modification_instructions_html)

            # Retrieve the metadata of the html webpage to give css AI context
            metadata = template_bot.get_metadata(updated_html)

            # Then do css
            modification_instructions_css = (
                f"Given the newly modified HTML structure: {metadata}, create CSS updates that align with the changes"
                f"and user preferences. Focues on applying styles for new classes or IDs, adjust color schemes, "
                f"typography, and layout responsiveness as per the user's feedback. Ensure the CSS enhances the page's "
                f"visual appeal and user interaction, adhering to modern web design principles."
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
        self.skip_node = "AboutPage"


class AboutPage(BasePageModification):
    def __init__(self, name, next_node='ProductPage', requires_input=True):
        super().__init__(name, page_name='About', next_node=next_node, requires_input=requires_input)
        self.skip_node = "ProductPage"


class ProductPage(BasePageModification):
    def __init__(self, name, next_node='ContactPage', requires_input=True):
        super().__init__(name, page_name='Product', next_node=next_node, requires_input=requires_input)
        self.skip_node = "ContactPage"


class ContactPage(BasePageModification):
    def __init__(self, name, next_node='FinalMessage', requires_input=False):
        super().__init__(name, page_name='Contact', next_node=next_node, requires_input=requires_input)
        self.skip_node = "FinalMessage"

    def request_changes(self, state_manager, user_input):
        # Call the base implementation to set up the common parts
        base_result = super().request_changes(state_manager, user_input)

        if user_input is None:
            # Customizing the skip button message for the ContactPage
            buttons = [{'name': 'End Conversation', 'value': 'skip'}]
            # Update the result dictionary with the customized buttons
            base_result.update({'buttons': buttons})

        return base_result

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
