const socket = io.connect('http://localhost:5000');  // Adjust the URL as needed


// Append messages to the chat history
function appendMessage(message, sender) {
    const chatContainer = document.getElementById('chatHistory');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
     // Check if 'message' is an object and has the 'text' property
    const messageText = typeof message === 'object' && message.text ? message.text : message;
    messageDiv.textContent = messageText;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the latest message
}

// Function to initiate the conversation
function startConversation() {
    socket.emit('start_conversation');

}

// Function to send a user message to the server
function sendMessage(message) {
    socket.emit('user_response', { message: message });
}

// Function to handle incoming messages from the server
socket.on('conversation_update', (data) => {
    console.log(data) // Debug

    // Check if its a popup action first to prevent appending the message to the chat container
    if (data.action === 'show_popup' && data.buttons && data.message) {
        displayPopup(data.message, data.buttons);
    } else {
        // Handle normal message appending and input enabling/disabling
        if (data.message) {
        appendMessage(data.message, 'bot');
    }
    if (data.generatedText) {
        appendMessage(data.generatedText, 'bot');
    }

    if (data.response_type === 'text') {
        enableInput();
    } else if (data.response_type === 'button' && data.buttons) {
        displayChoices(data.buttons);
    } else if (data.response_type === null) {
        disableInput();
    }
    }
    console.log(data) // Debug
    // Handle other types of data (e.g., 'generatedCode') as needed
});

document.addEventListener('DOMContentLoaded', () => {
    startConversation(); // Start the conversation when the page loads

    const sendButton = document.getElementById('sendBtn');
    const chatInput = document.getElementById('chatInput');

    sendButton.addEventListener('click', () => {
        const message = chatInput.value.trim();
        if (message) {
            appendMessage(message, 'user');
            sendMessage(message);
            chatInput.value = ''; // Clear the input after sending
        }
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); // Prevent the default action to avoid form submission
            sendButton.click(); // Trigger the send button click event
        }
    });
});

function disableInput() {
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendBtn');
    // Disable the input field and button
    chatInput.disabled = true;
    sendButton.disabled = true;
}

function enableInput() {
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendBtn');
    // Disable the input field and button
    chatInput.disabled = false;
    sendButton.disabled = false;
}


function displayChoices(buttons) {
    buttons.forEach(button => {
        const buttonElement = document.createElement('button');
        buttonElement.textContent = button.name;
        buttonElement.className = 'chat-button';
        buttonElement.onclick = () => {
            appendMessage({ text: button.name, sender: 'user' }); // Display button text as user message
            sendMessage(button.value); // Send the button's value to the backend
            clearButtons();
        };
        document.getElementById('chatHistory').appendChild(buttonElement);
    });
}

function displayPopup(message, buttons) {
    // Find the chat history container
    const chatHistoryContainer = document.getElementById('chatHistory');

    // Create the popup container
    const popupContainer = document.createElement('div');
    popupContainer.id = 'popupContainer';
    popupContainer.className = 'popup-container';

    // Create the popup content container
    const popup = document.createElement('div');
    popup.className = 'popup';
    popupContainer.appendChild(popup);

    // Add message to the popup
    const popupMessage = document.createElement('p');
    popupMessage.id = 'popupMessage';
    popupMessage.textContent = message;
    popup.appendChild(popupMessage);

     // Create buttons and add to the popup
    buttons.forEach(button => {
        const buttonElement = document.createElement('button');
        buttonElement.textContent = button.name;
        buttonElement.onclick = () => {
            sendMessage(button.value);
            popupContainer.style.display = 'none';
            document.body.removeChild(popupContainer); // Remove popup after use
        };
        popup.appendChild(buttonElement);
    });

    // Append the popup container to the chat history div
    chatHistoryContainer.appendChild(popupContainer);

    // Show the popup
    popupContainer.style.display = 'flex';
 }

function clearButtons() {
    document.querySelectorAll('.chat-button').forEach(button => button.remove());
}


///////////////////////////////////////////////////////////////////
//IFRAME JS
//////////////////////////////////////////////////////////////////

document.addEventListener('DOMContentLoaded', function() {
    // Retrieve the selected template type from local storage
    const selectedTemplateType = localStorage.getItem('selectedTemplateType');

    if (selectedTemplateType) {
        // Request the template details from the server via WebSocket
        socket.emit('request_template', { type: selectedTemplateType });

        // Clear the selected template type from local storage to avoid unintended reuse
        localStorage.removeItem('selectedTemplateType');
    }

    // Handle the server response with the template information
    socket.on('template_response', function(data) {
        if (data.templateId && data.initialPageContent) {
            // Store the templateId in local storage
            localStorage.setItem('currentTemplateId', data.templateId);
            loadPageContent('Home');
        } else {
            console.error('Error fetching template:', data.error);
            // Handle error, such as showing a notification to the user
        }
    });
});

// Message listener for navigation within the iframe
window.addEventListener('message', function(event) {
    // Optional: Check event.origin here for security
    if (event.data.type === 'navigate') {
        loadPageContent(event.data.pageName);
    }
});

// Function to load specific page content into the iframe
function loadPageContent(pageName) {
    // Retrieve the templateId from local storage
    const templateId = localStorage.getItem('currentTemplateId');
    if (templateId) {
        const previewFrame = document.getElementById('previewFrame');
        const pageUrl = `/template_content/${templateId}/${pageName}`;
        previewFrame.src = pageUrl;
    }
}

socket.on('update_template', function(data) {
    const iframe = document.getElementById('previewFrame');
    if (iframe && iframe.contentWindow && iframe.contentWindow.document) {
        const iframeDoc = iframe.contentWindow.document;
        iframeDoc.open();
        iframeDoc.write(data.template);
        iframeDoc.close();
    } else {
        console.error("Iframe document is not accessible");
    }
});

// Listen for an event indicating that the iframe should be refreshed
socket.on('refresh_iframe', function() {
    refreshIframe();
});

// Function to refresh iframe content
function refreshIframe() {
    const iframe = document.getElementById('previewFrame');
    iframe.contentWindow.location.reload(true);
}




