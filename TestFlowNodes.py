from OpenCAI import Node
from flask import session, request

testNodeData1 = {"NodeName": "TestNode1 - Intro",
                 "AITextGenerationPrompt": "Generate a brief greeting message that introduces you as an automated "
                                           "web designer named 'Elaa'. The message should not be longer than 3 "
                                           "sentences and the message should not be open-ended.",
                 "AICodeGenerationPrompt": "",
                 "DefaultSystemPrompt": "",
                 "DynamicPrompt": "",
                 "TextResponse": False,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": "",
                 "TransitionTime": 5,
                 "FrontEndAction": ""

                 }
testNode1 = Node(testNodeData1)


def node_two_prompt():
    template_type = session.get('website_type', 'default')
    print(f"template-type:{template_type}")
    return f"I see that you want to build a {template_type} website. Let's get started."


testNodeData2 = {"NodeName": "TestNode2 - Confirm Website Type",
                 "AITextGenerationPrompt": "",
                 "AICodeGenerationPrompt": "",
                 "DefaultSystemPrompt": "",
                 "DynamicPrompt": node_two_prompt,
                 "TextResponse": False,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": "",
                 "TransitionTime": 5,
                 "FrontEndAction": ""
                 }
testNode2 = Node(testNodeData2)

testNodeData3 = {"NodeName": "TestNode3 - Website Name",
                 "AITextGenerationPrompt": "Generate a brief message asking the user what they would like to name their"
                                           "website. Given the type of website. Furthermore, make sure the message gets"
                                           "to the point- no small talk. ",
                 "AICodeGenerationPrompt": "",
                 "DefaultSystemPrompt": "",
                 "DynamicPrompt": "",
                 "TextResponse": True,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": "",
                 "TransitionTime": 10,
                 "FrontEndAction": ""
                 }
testNode3 = Node(testNodeData3)

testNodeData4 = {"NodeName": "TestNode4 - Extract Home Page",
                 "AITextGenerationPrompt": "",
                 "AICodeGenerationPrompt": "Given template type as {template_type} and website name from the user. "
                                           "Modify the home page HTML to include the website name. "
                                           "Do not change any other thing.",
                 "DefaultSystemPrompt": "Please wait while we customize the home page...",
                 "DynamicPrompt": "",
                 "TextResponse": False,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": "TestNode3 - Website Name",
                 "TransitionTime": 10,
                 "FrontEndAction": {
                     "action": "extractHTML",
                     "targetPage": "home",
                 }
                 }
testNode4 = Node(testNodeData4)


testNodeData5 = {"NodeName": "TestNode5 - Send confirmation",
                 "AITextGenerationPrompt": "",
                 "AICodeGenerationPrompt": "",
                 "DefaultSystemPrompt": "We have added the website name to the given template.",
                 "DynamicPrompt": "",
                 "TextResponse": True,
                 "ButtonResponse": False,
                 "AdaptiveCodeGeneration": "TestNode3 - Website Name",
                 "TransitionTime": 0,
                 "FrontEndAction": ""
                 }
testNode5 = Node(testNodeData5)

testNodes = [testNode1, testNode2, testNode3, testNode4, testNode5]
