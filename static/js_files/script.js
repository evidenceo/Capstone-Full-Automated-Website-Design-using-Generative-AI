const socket = io.connect('http://localhost:5001');  // Adjust the URL as needed


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
        } else if (data.response_type === 'hybrid') {
            enableInput();
            displayChoices(data.buttons);
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
    // Clear buttons before displaying new ones
    clearButtons();

    buttons.forEach(button => {
        const buttonElement = document.createElement('button');
        buttonElement.textContent = button.name;
        buttonElement.className = 'chat-button';
        buttonElement.setAttribute('data-active', 'true'); // Mark as active button
        buttonElement.onclick = () => {
            appendMessage({ text: button.name, sender: 'user' }); // Display button text as user message
            sendMessage(button.value); // Send the button's value to the backend
        };
        document.getElementById('chatHistory').appendChild(buttonElement);
    });
}

function displayPopup(message, buttons) {
    // Find the chat history container
    const chatHistoryContainer = document.getElementById('chatHistory');

    // Check if a popup already exists and remove it
    let existingPopup = document.getElementById('popupContainer');
    if (existingPopup) {
        existingPopup.remove();
    }

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
        buttonElement.onclick = (event) => {
            // Prevent default form submission and stop event propagation
            event.preventDefault();
            event.stopPropagation();

            // Remove popup from DOM
            chatHistoryContainer.removeChild(popupContainer);

            // Send the button's value to the backend
            sendMessage(button.value);
        };
        popup.appendChild(buttonElement);
    });

    // Append the popup container to the chat history div
    chatHistoryContainer.appendChild(popupContainer);

    // Show the popup
    popupContainer.style.display = 'flex';
 }

function clearButtons() {
    document.querySelectorAll('.chat-button[data-active="true"]').forEach(button => {
        button.remove();
    });
}

///////////////////////////////////////////////////////////////////
//IFRAME JS
//////////////////////////////////////////////////////////////////

// This is to load the template into the iframe
document.addEventListener('DOMContentLoaded', function() {
    loadTemplatePage('Home');
    // Store the templateId in local storage
    localStorage.setItem('currentTemplateId', data.templateId);
});


// Message listener for navigation within the iframe
window.addEventListener('message', function(event) {
    // Optional: Check event.origin here for security
    if (event.data.type === 'navigate') {
        loadTemplatePage(event.data.pageName);
    }
});

// Function to load specific page content into the iframe
function loadTemplatePage(pageName) {
    if (!userTemplateId) return; // Ensure the template ID is available

    if (userTemplateId) {
        const iframe = document.getElementById('previewFrame');
        const doc = iframe.contentWindow.document;
        const pageUrl = `/template_preview/html/${userTemplateId}/${pageName}`;
        previewFrame.src = pageUrl;
    }
}

// Listen for an event indicating that the iframe should be refreshed
socket.on('refresh_iframe', function() {
    refreshIframe();
});

// Function to refresh iframe content
function refreshIframe() {
    const iframe = document.getElementById('previewFrame');
    const currentSrc = iframe.src;
    iframe.src = "{{ url_for('conversation') }}";
    iframe.src = currentSrc;
}

// Listen to event to load
socket.on('show_loading', data => {
    console.log(data.message);
    // Show the loading indicator
    document.getElementById('previewOverlay').style.display = 'block';
});

// Listen for the hide loading
socket.on('hide_loading', data => {
    console.log(data.message);
    // Hide the loading indicator
    document.getElementById('previewOverlay').style.display = 'none';
});








