from OpenCAI import CAIFlow
from TestFlowNodes import *


# Test File for Building the Conversational Flow
def conversation_flow():
    testFlow = CAIFlow()
    testFlow.registerNodes(testNodes)
    # testFlow.printRegisteredNodes()

    testFlow.appendNode("TestNode1 - Intro", {"": testNode2.nodeName})
    testFlow.appendNode(testNode2.nodeName, {"": testNode3.nodeName})
    testFlow.appendNode(testNode3.nodeName, {"": testNode4.nodeName})
    testFlow.appendNode(testNode4.nodeName, {"": testNode5.nodeName})

    return testFlow

