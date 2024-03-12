document.addEventListener('DOMContentLoaded', () => {
    startConversation(); // Start the conversation when the page loads
    const sendButton = document.getElementById('sendBtn');
    const chatInput = document.getElementById('chatInput');
    const chatHistory = document.getElementById('chatHistory');

    sendButton.addEventListener('click', () => {
        const message = chatInput.value.trim();
        if (message) {
            appendMessage(message, 'user');
            sendMessage(message); // Send the user message to the server
            chatInput.value = '';  // Clear the input field.
        }
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();  // Prevent form submission.
            const message = chatInput.value.trim();
            if (message) {
                appendMessage(message, 'user');
                sendMessage(message); // Send the user message to the server
                chatInput.value = '';  // Clear the input field.
            }
        }
    });
});

function startConversation() {
    // Initialize the conversation without any user message
    sendMessage('');
}

// Function to handle sending a message
    function sendMessage(message) {
        fetch('/conversation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
           receiveMessage(data); // Process the data received from the server
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

function receiveMessage(data) {
    appendMessage(data.GeneratedText, 'bot');
    // Handle FrontEndAction if present
    if (data.FrontEndAction) {
        handleFrontEndAction(data.FrontEndAction);
    } else {
        // Check if both TextInput and ButtonsInput indicate no user response is needed
        if (data.UserInputOptions.TextInput === false && data.UserInputOptions.ButtonsInput.length === 0) {
            // TransitionTime should be a number; ensure it's properly set in Node definitions
            const transitionTime = data.TransitionTime ? parseInt(data.TransitionTime, 10) : 0;
            // Automatically progress after the specified delay
            setTimeout(() => sendMessage(''), transitionTime * 1000);
        } else {
            // Handle cases where user input is required
            if (data.UserInputOptions.ButtonsInput.length > 0) {
                displayChoices(data.UserInputOptions.ButtonsInput);
            }
            document.getElementById('chatInput').disabled = !data.UserInputOptions.TextInput;
        }
    }
}

// Implement a function to handle FrontEndAction
function handleFrontEndAction(action) {
    switch (action.action) {
        case 'extractHTML':
            extractAndSendHTML(action.targetPage);
            break;
        // Handle other actions as needed
    }
}

// Function to extract HTML content from the iframe and send it back to the server
function extractAndSendHTML(targetPage) {
    var iframe = document.getElementById('previewFrame');
    if (iframe.contentWindow) {
        // Assuming same-origin policy is not an issue
        var htmlContent = iframe.contentWindow.document.documentElement.outerHTML;
        // Send the HTML content back to the server
        sendContentToServer(htmlContent, targetPage);
    }
}

// Function to send extracted content back to the server
function sendContentToServer(content, targetPage) {
    fetch('/receive_content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: content, targetPage: targetPage }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'Content received') {
            // Trigger the next step in the conversation indicating processing can start
            sendMessage("Next Node");
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Implement the updateIframeContent function if you decide to update parts of the iframe content
// This function would need details about how to find and update specific parts of your iframe's document
// function updateIframeContent(modifiedContent, targetPage) {
//     // Implementation depends on your iframe structure and how you wish to update it
// }


function appendMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageElement.className = sender === 'user' ? 'user-message' : 'bot-message';
    chatHistory.appendChild(messageElement);
}


function displayMessage({ text, sender }) {
    const chatContainer = document.getElementById('chatHistory');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = text;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function displayChoices(buttons) {
    buttons.forEach(button => {
        const buttonElement = document.createElement('button');
        buttonElement.textContent = button.name;
        buttonElement.className = 'chat-button';
        buttonElement.onclick = () => {
            displayMessage({ text: button.name, sender: 'user' }); // Display button text as user message
            sendMessage(button.name); // Send the button's action to Voiceflow
            clearButtons();
        };
        document.getElementById('chatHistory').appendChild(buttonElement);
    });
}


function clearButtons() {
    document.querySelectorAll('.chat-button').forEach(button => button.remove());
}


///////////////////////////////////////////////////////////////////
//IFRAME JS
//////////////////////////////////////////////////////////////////

// Function to reload the preview iframe
function reloadPreview() {
    var previewFrame = document.getElementById('previewFrame');
    var currentSrc = previewFrame.src;
    previewFrame.src = '';
    previewFrameFrame.src = currentSrc;
}

// Function to load specific page content into the iframe
function loadPageContent(pageName) {
    var previewFrame = document.getElementById('previewFrame');
    // Construct the URL for the specific page
    var pageUrl = `/template_content/${templateId}/${pageName}`;
    previewFrame.src = pageUrl;
}

// Message listener for navigation within the iframe
window.addEventListener('message', function(event) {
    // Optional: Check event.origin here for security
    if (event.data.type === 'navigate') {
        loadPageContent(event.data.pageName);
    }
});

// Set the initial content of the iframe
document.addEventListener('DOMContentLoaded', function() {
    var previewFrame = document.getElementById('previewFrame');
    previewFrame.src = templateContentUrl; // Use the variable here
});