document.addEventListener('DOMContentLoaded', function() {
    const userTemplateId = document.body.getAttribute('data-user-template-id'); // Ideally this should not be hard-coded
    const pageName = 'Home';
    console.log(userTemplateId)

    // Initialize Froala Editor with options
    const editor = new FroalaEditor('#editor', {
        // Correct the toolbarButtons array
        toolbarButtons: ['codeView', 'color', 'textColor', 'backgroundColor', '|', 'bold', 'italic', 'underline', 'html'],
        // Correctly nest codeMirrorOptions inside codeViewOptions
        codeViewOptions: {
            codeMirror: true,
            codeMirrorOptions: {
                mode: 'htmlmixed',
                theme: 'material',
                lineNumbers: true,
                lineWrapping: true,
                indentUnit: 4,
                smartIndent: true,
                matchBrackets: true,
                autoCloseTags: true
            }
        },
        // Specify options as needed
        imageUploadURL: '/file-upload', // Make sure this endpoint is configured on the server
        events: {
            'image.uploaded': function (response) {
                // Handle the response from the image upload
            },
            'initialized': function () {
                // Load the template once Froala is initialized
                loadTemplate(userTemplateId, pageName, this);
            }
        }
    });

    // Setup event listeners
    setupEventListeners(editor);
});

function loadTemplate(userTemplateId, pageName, editorInstance) {
    // Construct the URL from which to load the HTML content
    const pageUrl = `/template_customize/html/${userTemplateId}/${pageName}`;
    fetch(pageUrl)
        .then(response => response.text())
        .then(html => {
            // Use Froala's method to set HTML content
            editorInstance.html.set(html);
        })
        .catch(error => console.error('Error loading template:', error));
}

function setupEventListeners(editor) {
    const colorPicker = document.getElementById('colorPicker');
    if (colorPicker) {
        colorPicker.addEventListener('change', function(event) {
            // Use Froala's methods to apply color
            editor.color.apply(event.target.value);
        });
    }
    // Additional listeners as needed, e.g., for a save button
    document.addEventListener('DOMContentLoaded', function() {
    const userTemplateId = document.body.getAttribute('data-user-template-id'); // Ideally this should not be hard-coded
    const pageName = 'Home';
    console.log(userTemplateId)

    // Initialize Froala Editor with options
    const editor = new FroalaEditor('#editor', {
        // Correct the toolbarButtons array
        toolbarButtons: ['codeView', 'color', 'textColor', 'backgroundColor', '|', 'bold', 'italic', 'underline', 'html'],
        // Correctly nest codeMirrorOptions inside codeViewOptions
        codeViewOptions: {
            codeMirror: true,
            codeMirrorOptions: {
                mode: 'htmlmixed',
                theme: 'material',
                lineNumbers: true,
                lineWrapping: true,
                indentUnit: 4,
                smartIndent: true,
                matchBrackets: true,
                autoCloseTags: true
            }
        },
        // Specify options as needed
        imageUploadURL: '/file-upload', // Make sure this endpoint is configured on the server
        events: {
            'image.uploaded': function (response) {
                // Handle the response from the image upload
            },
            'initialized': function () {
                // Load the template once Froala is initialized
                loadTemplate(userTemplateId, pageName, this);
            }
        }
    });

    // Setup event listeners
    setupEventListeners(editor);
});

function loadTemplate(userTemplateId, pageName, editorInstance) {
    // Construct the URL from which to load the HTML content
    const pageUrl = `/template_customize/html/${userTemplateId}/${pageName}`;
    console.log(pageUrl)
    fetch(pageUrl)
        .then(response => response.text())
        .then(html => {
            // Use Froala's method to set HTML content
            editorInstance.html.set(html);
        })
        .catch(error => console.error('Error loading template:', error));
}

function setupEventListeners(editor) {
    const colorPicker = document.getElementById('colorPicker');
    if (colorPicker) {
        colorPicker.addEventListener('change', function(event) {
            // Use Froala's methods to apply color
            editor.color.apply(event.target.value);
        });
    }
    // Additional listeners as needed, e.g., for a save button
    // Ensure you define a save button in your HTML for this listener to work
    const saveButton = document.getElementById('saveButton');
    if (saveButton) {
        saveButton.addEventListener('click', function() {
            // Retrieve the HTML content from Froala Editor
            const updatedHtml = editor.html.get();

            // Implement the AJAX request to send the updated HTML to your server
            fetch(`/save_template/${userTemplateId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ html: updatedHtml })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Template saved:', data);
                // Handle any post-save actions here
            })
            .catch(error => {
                console.error('Error saving template:', error);
            });
        });
    }
}
}