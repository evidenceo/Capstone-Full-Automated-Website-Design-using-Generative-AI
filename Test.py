from OpenCAI import *
from TestFlow import conversation_flow

# Test File for Running the Conversational Flow

# Instead of a while loop in runFlow3(), the code line 'response = testFlow.processNode(userInput)' and
# 'if response == {}: print("End of Flow")' will have to be placed in the appropriate endpoint where the JavaScript will
# send its acknowledgements.

def runFlow3():
    testFlow = conversation_flow()  # Initialize the conversation flow once outside the loop

    while True:
        userInput = input("Enter Input: ")
        response = testFlow.processNode(userInput)  # Use the same flow object for processing input

        if response == {}:
            print("End of Flow")
            break
        else:
            print(response)

runFlow3()


