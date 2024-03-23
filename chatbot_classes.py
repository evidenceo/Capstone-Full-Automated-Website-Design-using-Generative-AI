import openai  # pip install openai==0.28

with open("APIKey.txt", "r") as textFile:
    api_key = textFile.read().strip()  # Personal OpenAI product key
openAIModelVersion = "gpt-4"


class TemplateModificationBot:
    def __init__(self, api_key, model_version="gpt-4-turbo-preview"):
        self.api_key = api_key
        self.model_version = model_version
        openai.api_key = self.api_key

    def modify_html(self, original_html, modification_instructions):
        """
                Generate modified HTML template based on the given instructions.

                :param original_html: The original HTML template.
                :param modification_instructions: Instructions for how to modify the template.
                :return: The modified HTML template.
                """

        combined_instructions = f"Original HTML:\n{original_html}\n\nModification Instructions:\n{modification_instructions}"

        response = openai.ChatCompletion.create(
            model=self.model_version,
            messages=[
                {"role": "system",
                 "content": "You are a code generator. Your task is to modify a given HTML code based on the "
                            "instruction of the user without altering the rest of the code. Do not give any "
                            "explanations.Just generate HTML code based on instructions. For example, if the "
                            "instruction was change the website name to 'My New Website', think about the appropriate "
                            "places the website name should be in the code, add it and send the updated code back, "
                            "with no explanation or text generation of any kind. Just perform the task and send the "
                            "result."
                            "Do not alter any part of the code linking to other pages. "
                            "I repeat to not alter any other part of the code linking to other pages or files."},
                {"role": "user", "content": combined_instructions}
            ],
            temperature=0.2,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Assuming the AI response includes the modified HTML directly
        modified_html = response.choices[0].message["content"]
        return modified_html

    def modify_css(self, original_css, modification_instructions):
        """
          Generate modified CSS template based on the given instructions.

          :param original_css: The original CSS template.
          :param modification_instructions: Instructions for how to modify the template.
          :return: The modified CSS template.
        """

        combined_instructions = f"Original CSS:\n{original_css}\n\nModification Instructions:\n{modification_instructions}"

        response = openai.ChatCompletion.create(
            model=self.model_version,
            messages=[
                {"role": "system",
                 "content": "You are a code generator. Your task is to modify a given CSS code based on the "
                            "instruction of the user without altering the rest of the code. Return the answer in format"
                            " that can be directly loaded in an iframe without editing. In other words, do not give any"
                            " explanations or add any text.Just generate CSS code based on instructions and send the"
                            " result back. I repeat do not send any explanations, no altering original CSS without"
                            " direct instruction from user. Just perform the task and send the result back."
                 },
                {"role": "user", "content": combined_instructions}
            ],
            temperature=0.2,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Assuming the AI response includes the modified CSS directly
        modified_css = response.choices[0].message["content"]
        return modified_css

    def get_metadata(self, web_page):
        """
          Retrieve the metadata of the given webpage most likely HTML but who knowsss.

          :param web_page: The webpage we are getting the metadata.
          :return: The metadata of webpage.
        """

        response = openai.ChatCompletion.create(
            model=self.model_version,
            messages=[
                {"role": "system",
                 "content": "You retrieve metadata of website pages in json format"
                 },
                {"role": "user", "content": f"Generate detailed metadata for the HTML, including comments "
                                            f"that guide the CSS customization. The metadata should reflect the "
                                            f"structure, semantic elements used, areas designated for dynamic effects,"
                                            f" and any specific id/class names that will be targeted for styling. "
                                            f"This metadata will inform the CSS customization process, ensuring that "
                                            f"the styling precisely matches the layout's intended design and "
                                            f"interactive features. Here is the HTML code: {web_page}"
                 }
                ],
            temperature=0.2,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "json_object"}
        )

        # Assuming the AI response includes the modified CSS directly
        modified_css = response.choices[0].message["content"]
        return modified_css


template_bot = TemplateModificationBot(api_key=api_key)


class TextGenerationBot:
    def __init__(self, api_key, model_version="gpt-4-turbo-preview"):
        self.api_key = api_key
        self.model_version = model_version
        openai.api_key = self.api_key

    def dynamic_message(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model_version,
            messages=[
                {"role": "system",
                 "content": "You are a web developer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        result = response.choices[0].message["content"]
        return result

    def extraction(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model_version,
            messages=[
                {"role": "system",
                 "content": "You are a web developer gathering information from user."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        result = response.choices[0].message["content"]
        return result


text_bot = TextGenerationBot(api_key=api_key)

"""# Example usage
apiKey = api_key
chatbot = TemplateModificationBot(apiKey)

original_html = "<html><head><title>Example Site</title></head><body>Welcome to our site!</body></html>"
modification_instructions = "Change the title to 'My New Website' and add a paragraph saying 'This is my updated website using AI.'"
modified_html = chatbot.modify_html(original_html, modification_instructions)

print("Original HTML:\n", original_html)
print("\nModified HTML:\n", modified_html)"""
