import openai  # pip install openai==0.28


class OpenAIChatBot:

    def __init__(self, apiKey, openAIModelVersion, systemRole, systemContent):  # Class attributes
        self.apiKey = apiKey  # Personal OpenAI product key
        self.openAIModelVersion = openAIModelVersion  # GPT Model/Version to use
        self.systemRole = systemRole  # OpenAI system's contextual role
        self.systemContent = systemContent  # OpenAI's system's contextual instructions
        self.messageHistory = []  # Global table to keep track of the message history between the user and the system

    # Function to initialize the OpenAI chat box system configurations
    def setUpChatBot(self):
        self.messageHistory = []  # Clear message history
        openai.api_key = self.apiKey

        if self.systemRole and self.systemContent:  # If the system's role and content have been provided

            systemInfo = {"role": self.systemRole, "content": self.systemContent}  # The system's perceived role and
            # prompted behaviour
            self.messageHistory.append(systemInfo)  # Append the system's prompt to the message history to provide
            # the API this context

    # Function to generate a response to the most recent user prompt given the message history, and add the response
    # to the message history
    def generatePromptResponse(self, promptMessage):

        promptInfo = {"role": "user", "content": promptMessage}  # Compile user role and message into a dictionary
        self.messageHistory.append(promptInfo)  # Add the user prompt to the message history array

        promptResponseInfo = openai.ChatCompletion.create(model=self.openAIModelVersion, messages=self.messageHistory)
        # Receive the latest prompt response given the message history
        promptReply = promptResponseInfo.choices[0].message.content  # Opens the first response choice and displays
        # the message's content

        promptReplyInfo = {"role": self.systemRole, "content": promptReply}  # Compile system role and message into a
        # dictionary
        self.messageHistory.append(promptReplyInfo)  # Add the prompt response to the message history array

        return promptReply
