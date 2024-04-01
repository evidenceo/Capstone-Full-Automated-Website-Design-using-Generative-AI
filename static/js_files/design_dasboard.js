let editorWrapper = {
    editor: null,
    currentPageName: 'Home'
};

document.addEventListener('DOMContentLoaded', function() {
    const userTemplateId = document.body.getAttribute('data-user-template-id');
    console.log(userTemplateId);

    fetch(`/template/pages/${userTemplateId}`)
        .then(response => response.json())
        .then(availablePages => {
            initializeFroalaEditor(userTemplateId, availablePages);
        })
        .catch(error => console.error('Error fetching available pages:', error));
});

function initializeFroalaEditor(userTemplateId, availablePages) {
    const dropdownOptions = availablePages.reduce((options, page) => {
        options[page] = page;
        return options;
    }, {});

    const editor = new FroalaEditor('#editor', {
        toolbarButtons: ['insertImage', 'codeView', 'color', 'textColor', 'backgroundColor', 'pageSelector', '|', 'bold', 'italic', 'underline', 'html'],
        imageUploadURL: '/file-upload',
        iframe: true,
        imageUploadParams: {
            id: 'editor',
            user_template_id: userTemplateId
        },
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
        events: {
            'initialized': function () {
                editorWrapper.editor = this;
                loadTemplate(userTemplateId, editorWrapper.currentPageName, this);
            },
            'image.uploaded': function (response) {
                console.log('Image uploaded response:', response);
            },
            'image.inserted': function ($img, response) {
                console.log('Image inserted response:', response);
            },
            'image.replaced': function ($img, response) {
                console.log('Image replaced response:', response);
            }
        }
    });

    FroalaEditor.DefineIcon('pageSelector', {NAME: 'list'});
    FroalaEditor.RegisterCommand('pageSelector', {
        title: 'Select Page',
        type: 'dropdown',
        focus: false,
        undo: false,
        refreshAfterCallback: true,
        options: dropdownOptions,
        callback: function (cmd, val) {
            editorWrapper.currentPageName = val;
            if (editorWrapper.editor) {
                loadTemplate(userTemplateId, val, editorWrapper.editor);
            }
        }
    });

    setupEventListeners(userTemplateId);
}

function loadTemplate(userTemplateId, currentPageName, editorInstance) {
    const pageUrl = `/template_customize/html/${userTemplateId}/${currentPageName}`;
    fetch(pageUrl)
        .then(response => response.text())
        .then(html => {
            if (editorInstance) {
                editorInstance.html.set(html);
            } else {
                console.error("Editor instance is not available.");
            }
        })
        .catch(error => console.error('Error loading template:', error));
}

function setupEventListeners(userTemplateId) {
    const saveButton = document.getElementById('saveButton');
    if (saveButton) {
        saveButton.addEventListener('click', function() {
            const updatedHtml = editorWrapper.editor.html.get();
           // Use editor.currentPageName which holds the updated current page name
            fetch(`/save_page/${userTemplateId}/${editorWrapper.currentPageName}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ html: updatedHtml })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Template saved:', data);
                // Display the confirmation message
                saveConfirmation.style.display = 'inline';
                // Hide the confirmation message after 2 seconds
                setTimeout(() => {
                    saveConfirmation.style.display = 'none';
                }, 2000);
            })
            .catch(error => {
                console.error('Error saving template:', error);
            });
        });
    }
}

document.getElementById('publishButton').addEventListener('click', function() {
    const userTemplateId = document.body.getAttribute('data-user-template-id');
    window.fetch(`/download_template/${userTemplateId}`)
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        throw new Error('Download failed');
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "template.zip";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        alert('Download successful!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Download failed');
    });
});

