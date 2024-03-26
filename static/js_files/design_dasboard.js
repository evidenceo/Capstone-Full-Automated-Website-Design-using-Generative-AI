document.addEventListener('DOMContentLoaded', function() {
    const userTemplateId = document.body.getAttribute('data-user-template-id');
    const pageName = 'Home';
    console.log(userTemplateId);

    fetch(`/template/pages/${userTemplateId}`)
        .then(response => response.json())
        .then(availablePages => {
            initializeFroalaEditor(userTemplateId, availablePages, pageName);
        })
        .catch(error => console.error('Error fetching available pages:', error));
});

function initializeFroalaEditor(userTemplateId, availablePages, pageName) {
    const dropdownOptions = availablePages.reduce((options, page) => {
        options[page] = page;
        return options;
    }, {});

    FroalaEditor.DefineIcon('pageSelector', {NAME: 'list'});
    FroalaEditor.RegisterCommand('pageSelector', {
        title: 'Select Page',
        type: 'dropdown',
        focus: false,
        undo: false,
        refreshAfterCallback: true,
        options: dropdownOptions,
        callback: function (cmd, val) {
            loadTemplate(userTemplateId, val, this);
        }
    });

    const editor = new FroalaEditor('#editor', {
        toolbarButtons: ['insertImage', 'codeView', 'color', 'textColor', 'backgroundColor', 'pageSelector', '|', 'bold', 'italic', 'underline', 'html'],
        imageUploadURL: '/file-upload',
        imageUploadParams: { id: 'editor' },
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
                loadTemplate(userTemplateId, pageName, this);
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

    setupEventListeners(editor, userTemplateId, pageName);
}

function loadTemplate(userTemplateId, pageName, editorInstance) {
    const pageUrl = `/template_customize/html/${userTemplateId}/${pageName}`;
    fetch(pageUrl)
        .then(response => response.text())
        .then(html => {
            editorInstance.html.set(html);
        })
        .catch(error => console.error('Error loading template:', error));
}

function setupEventListeners(editor, userTemplateId, pageName) {
    const saveButton = document.getElementById('saveButton');
    if (saveButton) {
        saveButton.addEventListener('click', function() {
            const updatedHtml = editor.html.get();
            fetch(`/save_template/${userTemplateId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ html: updatedHtml })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Template saved:', data);
            })
            .catch(error => {
                console.error('Error saving template:', error);
            });
        });
    }
}
