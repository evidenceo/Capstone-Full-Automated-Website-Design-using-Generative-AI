from Chatbots import *
class Node:

    def __init__(self, nodeConfigurationData: dict) -> None:  # Class attributes

        # Initialization Data
        self.nodeName = nodeConfigurationData["NodeName"]
        self.aiTextGenerationPrompt = nodeConfigurationData["AITextGenerationPrompt"]
        self.aiCodeGenerationPrompt = nodeConfigurationData["AICodeGenerationPrompt"]
        self.defaultSystemPrompt = nodeConfigurationData["DefaultSystemPrompt"]
        self.textResponse = nodeConfigurationData["TextResponse"]
        self.buttonResponse = nodeConfigurationData["ButtonResponse"]
        self.adaptiveCodeGeneration = nodeConfigurationData["AdaptiveCodeGeneration"]
        self.transitionTime = nodeConfigurationData["TransitionTime"]
        self.dynamicPrompt = nodeConfigurationData.get("DynamicPrompt", None)
        self.frontEndAction = nodeConfigurationData.get("FrontEndAction", None)

        # Configuration Data
        self.responsePaths = {}

        # Default Data
        self.userResponse = ""
        self.parentNodes = {}
        self.nextNode = None
        self.previousNode = None

    def get_dynamic_prompt(self, *args, **kwargs):
        # Assuming 'self.dynamicPrompt' can be a callable or a static value
        if callable(self.dynamicPrompt):
            return self.dynamicPrompt(*args, **kwargs)  # Call if it's callable
        return self.dynamicPrompt  # Return as is if not callable


class CAIFlow:

    def __init__(self) -> None:  # Class attributes
        self.flowStart = None
        self.registeredNodes = {}
        self.currentNode = None
        self.processNodeCounter = 2
        self.processNodeCounterRange = self.processNodeCounter + 1

    def registerNodes(self, nodesToRegister: []):

        for node in nodesToRegister:
            nodeID = {node.nodeName: node}
            self.registeredNodes.update(nodeID)

    def appendNode(self, nodeName: str, userResponsePaths: dict) -> None:

        node = self.registeredNodes[nodeName]

        # If no nodes are in the conversational flow yet
        if self.flowStart is None:
            self.flowStart = node

        # Register response paths to node
        node.responsePaths = userResponsePaths

        for response in node.responsePaths:
            childNodeName = node.responsePaths[response]
            childNode = self.registeredNodes[childNodeName]

            childNode.parentNodes.update({childNodeName: response})

    def traverseFlow(self):

        if self.currentNode is None:
            self.currentNode = self.flowStart
            print(self.currentNode)
        else:
            self.currentNode = self.currentNode.nextNode
            print(self.currentNode)

    def generateText(self) -> str:

        # Generate the chatbot text given the node's text generation prompt and print it out
        if self.currentNode.aiTextGenerationPrompt != "":

            textPrompt = textGenerationChatBotObject.generatePromptResponse(self.currentNode.aiTextGenerationPrompt)

        # Print out the given the node's default system prompt if no AI generation was specified
        else:
            textPrompt = self.currentNode.defaultSystemPrompt

        return textPrompt

    def getUserInputOptions(self):
        inputOptions = {"TextInput": self.currentNode.textResponse, "ButtonsInput": []}

        if self.currentNode.buttonResponse:
            buttonOptions = [responseKey for responseKey, _ in self.currentNode.responsePaths.items()]
            inputOptions["ButtonsInput"] = buttonOptions

        return inputOptions

    def registerUserResponse(self, userResponse) -> str:

        self.currentNode.userResponse = userResponse
        return ""


    def set_current_node_by_name(self, node_name):
        if node_name in self.registeredNodes:
            self.currentNode = self.registeredNodes[node_name]
            print(self.currentNode)
        else:
            print("Node name not found in registered nodes.")

    def setNextNode(self):

        responsePaths = self.currentNode.responsePaths

        if responsePaths is not None:

            numberOfPaths = len(responsePaths)

            if numberOfPaths == 1:
                self.currentNode.nextNode = self.registeredNodes[next(iter(responsePaths.values()), None)]

            elif numberOfPaths > 1:

                userResponsePrompt = "["

                for key, value in responsePaths.items():
                    userResponsePrompt = userResponsePrompt + key + ", "

                userResponsePrompt = (userResponsePrompt[:len(userResponsePrompt) - 2] + "], "
                                      + self.currentNode.userResponse)

                userIntent = userIntentClassifierChatBotObject.generatePromptResponse(userResponsePrompt)
                self.currentNode.nextNode = self.registeredNodes[responsePaths[userIntent]]

    def generateCode(self, content="") -> str:  # content can be html, css and js
        if self.currentNode.aiCodeGenerationPrompt:
            # Construct the prompt to include HTML content and user input
            prompt = self.currentNode.aiCodeGenerationPrompt.format(content=content,
                                                                    user_input=self.currentNode.userResponse)

            # If the node requires adaptive code generation
            if self.currentNode.adaptiveCodeGeneration:
                userInput = self.registeredNodes[self.currentNode.adaptiveCodeGeneration].userResponse
                # Construct the prompt with both the content and the user input
                adaptivePrompt = "{}, {}".format(prompt, userInput)
                # Generate the adapted prompt
                adaptedPrompt = adaptiveCodeGenerationChatBotObject.generatePromptResponse(adaptivePrompt)
                # Use the adapted prompt for code generation
                codeGenerationResult = codeGenerationChatBotObject.generatePromptResponse(adaptedPrompt)
            else:
                # Directly use the constructed prompt if no adaptive code generation is needed
                codeGenerationResult = codeGenerationChatBotObject.generatePromptResponse(prompt)

            print(codeGenerationResult)
            return codeGenerationResult
        else:
            return ""

    def processNode(self, userResponse="", content="", targetPage=""):
        if not self.currentNode:
            self.currentNode = self.flowStart

        print(f"{self.currentNode.responsePaths}") # response paths already shows what path the node is supposed to
        # follow, essentially the next node
        print(f"{content} in processNode")

        # Register user's response for the current node.
        # This is crucial for nodes that depend on user's input for dynamic prompts or decisions.
        self.registerUserResponse(userResponse)

        returnInfo = {"GeneratedText": "", "UserInputOptions": self.getUserInputOptions(), "GeneratedCode": ""}

        # Check for FrontEndAction and prepare response for it
        if hasattr(self.currentNode, "frontEndAction") and self.currentNode.frontEndAction:
            # Assuming frontEndAction structure: { "action": "extractHTML", "targetPage": "home", ... }
            actionInfo = self.currentNode.frontEndAction
            returnInfo["FrontEndAction"] = actionInfo
            # Frontend will take the necessary action and POST back to another endpoint with results
            # save the response path of that this node takes because that is what would be the next node that
            # processing would start
            next_node = self.currentNode.nextNode
        else:
            # Handle dynamic prompts or use default system prompt to generate text.
            dynamicPrompt = self.currentNode.get_dynamic_prompt()
            generatedText = dynamicPrompt() if callable(dynamicPrompt) else dynamicPrompt
            if not generatedText:
                returnInfo["GeneratedText"] = self.generateText()

            # Generate code if the current node requires it.
            if self.currentNode.aiCodeGenerationPrompt:
                if userResponse == "Next Node":
                    # get the saved "nextnode of the previous node" start from this node
                    # 'content' should be stored in sessionmanager class
                    generatedCode = self.generateCode(content)
                    returnInfo["generatedCode"] = generatedCode

        # Determine the next node based on user's response and set it as the current node.
        if userResponse in self.currentNode.responsePaths:
            nextNodeName = self.currentNode.responsePaths[userResponse]
            self.currentNode = self.registeredNodes[nextNodeName]
        elif '' in self.currentNode.responsePaths:
            # Handle the default transition if the response does not match any key explicitly.
            nextNodeName = self.currentNode.responsePaths['']
            self.currentNode = self.registeredNodes[nextNodeName]

        # Optionally advance the flow automatically if no user input is required.
        if not self.currentNode.textResponse and not self.currentNode.buttonResponse:
            self.setNextNode()

        return returnInfo


class SessionManager:
    def __init__(self, session):
        self.session = session

    def get_content(self):
        return self.session.get('content', '')

    def get_target_page(self):
        return self.session.get('targetPage', '')

    def set_content_and_target_page(self, content, target_page):
        self.session['content'] = content
        self.session['targetPage'] = target_page

    def clear_content_and_target_page(self):
        self.session.pop('content', None)
        self.session.pop('targetPage', None)