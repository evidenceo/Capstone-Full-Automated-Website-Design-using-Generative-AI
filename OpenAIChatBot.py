import openai  # pip install openai==0.28


class OpenAIChatBot:

    def __init__(self, apiKey, openAIModelVersion, systemRole, systemContent, maxHistorySize=10):  # Class attributes
        self.apiKey = apiKey  # Personal OpenAI product key
        self.openAIModelVersion = openAIModelVersion  # GPT Model/Version to use
        self.systemRole = systemRole  # OpenAI system's contextual role
        self.systemContent = systemContent  # OpenAI's system's contextual instructions
        self.messageHistory = [{"role": "system",
                                "content": systemContent}]  # Global table to keep track of the message history between the user and the system
        self.maxHistorySize = maxHistorySize
        openai.api_key = self.apiKey
        self.reset_history()

    def update_system_context(self, role=None, content=None):  # Allows for dynamic updates to system's role and content
        if role:
            self.systemRole = role
        if content:
            self.systemContent = content
        self.reset_history()

    def append_to_history(self, role, content):
        # Ensure the history does not exceed the maximum size
        if len(self.messageHistory) > self.maxHistorySize:
            self.messageHistory.pop(0)  # Remove the oldest entry
        self.messageHistory.append({"role": role, "content": content})

    def generate_prompt_response(self, prompt_message):
        self.append_to_history("user", prompt_message)

        # Generate response using the OpenAI Chat Completions API
        response = openai.ChatCompletion.create(
            model=self.openAIModelVersion,
            messages=self.messageHistory,
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract and return the text of the response
        reply = response.choices[0].message["content"]
        self.append_to_history("system", reply)
        return reply

    def reset_history(self):
        self.messageHistory = [{"role": "system", "content": self.systemContent}]
        print("Initial context set.")  # Debug print to confirm this runs
