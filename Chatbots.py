from OpenAIChatBot import OpenAIChatBot

with open("APIKey.txt", "r") as textFile:
    openAIAPIKey = textFile.read().strip()  # Personal OpenAI product key
openAIModelVersion = "gpt-3.5-turbo"  # GPT Version to use

textGenerationChatBotInfo = {"role": "assistant", "content": "You are a message writer working for a client. The client"
                                                             " will give you instructions on what should be written "
                                                             "and your job is to generate a message that naturally "
                                                             "incorporates the client's instructions. Furthermore, the"
                                                             " message should be written in such a way that would make"
                                                             " the messages seem like they are part of a one on one "
                                                             "conversation."}

codeGenerationChatBotInfo = {"role": "assistant", "content": "You are a webdesign coder working for a client. The code"
                                                             " you produce is in HTML, embedded CSS, and embedded "
                                                             "JavaScript. The client will inform you of what the "
                                                             "webpage should look like and your code should reflect "
                                                             "these requests. Do not provide anything other than the "
                                                             "code."}

userIntentClassifierChatBotInfo = {"role": "assistant", "content": "You are a message intention classifier for a "
                                                                   "client. The client will give you an array of "
                                                                   "words along with a message (they will be "
                                                                   "separated by a comma). Analyze the message to "
                                                                   "understand its contextual intention. Afterwards, "
                                                                   "choose a word from the provided array that best "
                                                                   "represents the contextual intention of the "
                                                                   "provided message, and return that one word as "
                                                                   "your response. Nothing other but the word should "
                                                                   "be your response, and your response must be one "
                                                                   "of the case sensitive words belonging to the "
                                                                   "provided array. Ensure there are no quotation "
                                                                   "marks in your response. For example, if the "
                                                                   "client gives you the input '[morning, afternoon, "
                                                                   "evening, night], it is dark but I can still see "
                                                                   "some natural light. the '[morning, afternoon, "
                                                                   "evening, night]' portion of the client input "
                                                                   "represents the array and the 'it is dark but I "
                                                                   "can still see some natural light' portion of the "
                                                                   "client input represents the message. The word in "
                                                                   "the array that best describes the message intent "
                                                                   "is 'evening' so your response should simply be "
                                                                   "'evening'. The response 'Evening' is an invalid "
                                                                   "response because it does not match the case "
                                                                   "sensitivity of the word in the array."}

adaptiveCodeGenerationChatBotInfo = {"role": "assistant", "content": "You are a prompt engineer for a client. The "
                                                                     "client will give you a generative prompt along "
                                                                     "with a user message. The two will be put in "
                                                                     "separate curly braces separated by a comma, where"
                                                                     " the first text encapsulated by the curly braces "
                                                                     "is the generative prompt and the second text "
                                                                     "encapsulated by the curly braces is the message. "
                                                                     "Analyze the generative prompt to understand what "
                                                                     "its general generative objectives are, and then "
                                                                     "analyze the message to extract the details that "
                                                                     "may be relevant to the context of the generative "
                                                                     "prompt. Return a new generative prompt such that"
                                                                     " it maintains the general expected output of the "
                                                                     "original generative prompt but includes the "
                                                                     "relevant details provided from the message by "
                                                                     "substituting those details in for the general "
                                                                     "details in the original generative prompt. For "
                                                                     "example, if the client inputs '{Generate an image"
                                                                     "of a city park}, {the sky should be sunset}', "
                                                                     "an appropriate response to return would be "
                                                                     "'Generate an image of a city park with a sunset "
                                                                     "sky.' Another example is if the client inputs '{"
                                                                     "Generate a Python loop that prints the current "
                                                                     "iteration and loops as much as the user requests}"
                                                                     ", {i want it 100 times}', then an appropriate "
                                                                     "response to return would be 'Generate a Python "
                                                                     "loop that loops 100 times and prints the current "
                                                                     "iteration each time.'"}

textGenerationChatBotObject = OpenAIChatBot(apiKey=openAIAPIKey,
                                            openAIModelVersion=openAIModelVersion,
                                            systemRole=textGenerationChatBotInfo["role"],
                                            systemContent=textGenerationChatBotInfo["content"])

codeGenerationChatBotObject = OpenAIChatBot(apiKey=openAIAPIKey,
                                            openAIModelVersion=openAIModelVersion,
                                            systemRole=codeGenerationChatBotInfo["role"],
                                            systemContent=codeGenerationChatBotInfo["content"])

userIntentClassifierChatBotObject = OpenAIChatBot(apiKey=openAIAPIKey,
                                                  openAIModelVersion=openAIModelVersion,
                                                  systemRole=userIntentClassifierChatBotInfo["role"],
                                                  systemContent=userIntentClassifierChatBotInfo["content"])

adaptiveCodeGenerationChatBotObject = OpenAIChatBot(apiKey=openAIAPIKey,
                                                    openAIModelVersion=openAIModelVersion,
                                                    systemRole=adaptiveCodeGenerationChatBotInfo["role"],
                                                    systemContent=adaptiveCodeGenerationChatBotInfo["content"])

textGenerationChatBotObject.setUpChatBot()
codeGenerationChatBotObject.setUpChatBot()
userIntentClassifierChatBotObject.setUpChatBot()
adaptiveCodeGenerationChatBotObject.setUpChatBot()

nodeConfigurationDataExample = {"NodeName": "", "AITextGenerationPrompt": "", "AICodeGenerationPrompt": "",
                                "DefaultSystemPrompt": "", "TextResponse": False, "ButtonResponse": False,
                                "AdaptiveCodeGeneration": "", "TransitionTime": 0}

