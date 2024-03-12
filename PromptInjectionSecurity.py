from fuzzywuzzy import fuzz
import concurrent.futures
import random
from OpenAIChatBot import OpenAIChatBot

with open("APIKey.txt", "r") as textFile:
    openAIAPIKey = textFile.read().strip() # Personal OpenAI product key
openAIModelVersion = "gpt-3.5-turbo"  # GPT Version to use

# The system's perceived role via the prompts in the "content" key
# True if it isn't injection, false if it is
topicRelevancySystemInfo = {"role": "assistant", "content": "You are a web designer interviewing a client. The client "
                                                            "may make a request or statement that is unrelated to the "
                                                            "web design process. If the client makes such a remark, "
                                                            "respond with the one word 'False'. Otherwise, if the "
                                                            "request or statement is related to web design, respond "
                                                            "with the one word 'True'. For example, if the user writes "
                                                            "'Can you tell me what the weather is' or 'Tell me a cake "
                                                            "recipe', or 'Hi', then you must respond with 'False', but"
                                                            " a request made by the user such as 'I would like my "
                                                            "website to have room for a cake recipe' should be "
                                                            "responded with 'True' as it is a request related to the "
                                                            "design of a website. The client may not directly state "
                                                            "that the request or statement is for the website and may "
                                                            "mention a website component instead such as 'text' or "
                                                            "'name'. In this case, the topic is still relevant and "
                                                            "should be responded with 'True'."}

topicAppropriatenessSystemInfo = {"role": "assistant", "content": "You are a web designer interviewing a client. The "
                                                                  "client may make a request or statement that is "
                                                                  "inappropriate or unethical. If the client makes "
                                                                  "such a remark, respond with the one word 'False'. "
                                                                  "Otherwise, if the request or statement is indeed "
                                                                  "appropriate, respond with the one word 'True'. For "
                                                                  "example, if the user writes 'I want to make a human"
                                                                  " trafficking site' or 'I want room in this page for "
                                                                  "images of human slaughter', then you shall respond "
                                                                  "with 'False', but a request made by the user such "
                                                                  "as 'I want a comments section at the bottom of the "
                                                                  "screen' should be responded with 'True' as it is a "
                                                                  "request that is neither un-ethical or "
                                                                  "inappropriate. There may be cases where the "
                                                                  "request or statement contains inappropriate or "
                                                                  "unethical wording, but the context provided by the"
                                                                  "user proves the opposite. An example of such a case"
                                                                  "may be 'the human slaughter descriptions are "
                                                                  "disturbing' or 'this human trafficking site should "
                                                                  "be confronted by the government', or context "
                                                                  "indicative of reporting news or quotes. These examples "
                                                                  "contain unethical or inappropriate remarks but "
                                                                  "their intent is neither unethical or inappropriate "
                                                                  "given the context of the rest of the message. In "
                                                                  "such cases, respond with the one word 'True'."}

topicHarmfulnessSystemInfo = {"role": "assistant", "content": "You are a web designer interviewing a client. The client may make a request or statement that is harmful"}


# Create a chatbot object
chatBotTopicRelevancyObject = OpenAIChatBot(apiKey=openAIAPIKey,
                                            openAIModelVersion=openAIModelVersion,
                                            systemRole=topicRelevancySystemInfo["role"],
                                            systemContent=topicRelevancySystemInfo["content"])

# Create a chatbot object
chatBotTopicAppropriatenessObject = OpenAIChatBot(apiKey=openAIAPIKey,
                                                  openAIModelVersion=openAIModelVersion,
                                                  systemRole=topicAppropriatenessSystemInfo["role"],
                                                  systemContent=topicAppropriatenessSystemInfo["content"])


wordBlackList = ["arse", "arsehead", "arsehole", "ass", "asshole", "bastard", "bitch", "bloody", "bollocks",
                 "brotherfucker", "bullshit", "child-fucker", "cock", "crap", "cunt", "dickhead", "dyke",
                 "fatherfucker", "fuck", "fucker", "goddamn", "godsdamn", "hell", "horseshit", "kike", "motherfucker",
                 "nigga", "nigger", "negra", "negro", "pigfucker", "piss", "porn", "pornographic", "prick", "pussy",
                 "shit", "shite", "sisterfucker", "slut", "son of a whore", "son of a bitch", "turd", "twat", "wanker"]

topicRelevancyResponses = ["Your request is not relevant. Please try again.",

                           "Your inquiry lacks relevance. Kindly make another attempt",

                           "Your input is unrelated. Try again with a more relevant response.",

                           "The subject of your inquiry is not applicable. Please try a different and relevant input "
                           "or provide more context.",

                           "The inputted information is not applicable at the moment. Please try a different approach.",

                           "Your inquiry does not align with the current context. Please consider rephrasing or trying "
                           "a different input.",

                           "The content of your request is not pertinent. Please make another attempt with a more "
                           "relevant query.",

                           "Your query is off-topic. Please rephrase or provide something of more relevance.",

                           "The information you're looking for is not relevant to the current context. "
                           "Please try again with a more appropriate request.",

                           "Your request lacks relevance. Consider revising your query for a more suitable response."
                           ]

topicAppropriatenessResponses = ["Your request is inappropriate. Please try again.",

                                 "Your inquiry is not suitable. Please make another attempt.",

                                 "The nature of your request is inappropriate. Please try a different approach.",

                                 "The content of your request is not appropriate. Please make another attempt with a "
                                 "more suitable inquiry.",

                                 "Your inquiry is not in line with our guidelines. Try again with a more appropriate "
                                 "input.",

                                 "The subject matter of this request is inappropriate. Please consider rephrasing or "
                                 "inputting a more suitable query.",

                                 "Your input is not in accordance with our policies. Please try again with a more "
                                 "appropriate inquiry.",

                                 "What you're seeking is not suitable for this platform. Please try a different "
                                 "question.",

                                 "Your inquiry is deemed inappropriate. Kindly make another attempt with a more "
                                 "suitable input.",

                                 "The nature of your request is not acceptable. Please try again with a more "
                                 "appropriate query."
                                 ]


def detectAppropriateness(stringInput) -> bool:
    # Set up the chatbot
    chatBotTopicAppropriatenessObject.setUpChatBot()

    # ChatBot Response
    topicAppropriateness = chatBotTopicAppropriatenessObject.generatePromptResponse(stringInput)
    # print("Topic Appropriateness:", topicAppropriateness)

    if topicAppropriateness == "False":
        return False
    else:
        return True


def detectBlacklistedWords(stringInput) -> bool:
    matchingThreshold = 100
    stringInput = stringInput.split()

    for word in stringInput:
        for blackListedWord in wordBlackList:
            wordMatch = fuzz.token_set_ratio(word.lower(), blackListedWord.lower())

            if wordMatch >= matchingThreshold:
                return True

    return False


def detectRelevancy(stringInput) -> bool:
    # Set up the chatbot
    chatBotTopicRelevancyObject.setUpChatBot()

    # ChatBot Response
    topicRelevancy = chatBotTopicRelevancyObject.generatePromptResponse(stringInput)
    # print("Topic Relevancy:", topicRelevancy)

    if topicRelevancy == "False":
        return False
    else:
        return True


def selectInjectionDetectedMessage(promptInjectionSummary) -> str:

    selectedMessages = None

    if promptInjectionSummary["isTopicAppropriate"] is False:
        selectedMessages = topicAppropriatenessResponses
    elif promptInjectionSummary["isTopicRelevant"] is False:
        selectedMessages = topicRelevancyResponses

    numberOfMessages = len(selectedMessages) - 1
    messageIndex = random.randint(0, numberOfMessages)

    return selectedMessages[messageIndex]


while True:
    injectionDetected = False

    userInput = input("Enter a prompt: ")

    # injectionDetected = detectBlacklistedWords(userInput)
    # print(injectionDetected)

    userInputWords = userInput.split()

    for word in userInputWords:
        for blackListedWord in wordBlackList:
            wordMatch = fuzz.token_set_ratio(word.lower(), blackListedWord.lower())

            # if wordMatch >= 100:
                # injectionDetected = True
                # print(blackListedWord)

    if injectionDetected:
        print("Injection Detected: Blacklisted Word")
    else:
        print("No Injection Detected for Blacklisted Words")

        # Creating a ThreadPoolExecutor to multithread checks
        with concurrent.futures.ThreadPoolExecutor() as threadExecutor:

            # Detect if the topic is relevant
            isTopicRelevantThread = threadExecutor.submit(detectRelevancy, userInput)
            isTopicAppropriateThread = threadExecutor.submit(detectAppropriateness, userInput)

            # Wait for threads to complete and retrieve their results
            isTopicAppropriate = isTopicAppropriateThread.result()
            isTopicRelevant = isTopicRelevantThread.result()

        if isTopicRelevant and isTopicAppropriate:
            print("No Injection Detected")
        else:
            print("Injection Detected")

            injectionSummary = {"isTopicAppropriate": isTopicAppropriate, "isTopicRelevant": isTopicRelevant}
            injectionPromptMessage = selectInjectionDetectedMessage(injectionSummary)

            print("Injection summary:", injectionSummary)
            print(injectionPromptMessage)
