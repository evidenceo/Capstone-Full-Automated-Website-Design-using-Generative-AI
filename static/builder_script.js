//BUILDER.HTML
const socket = io.connect('http://localhost:5000');

function toggleOptions() {
    var options = document.getElementById("options");
    options.classList.toggle("hidden");
}

function redirectToMain(type) {
    // Store the selected template type in local storage
    localStorage.setItem('selectedTemplateType', type);
    // Send template type to server
     socket.emit('set_template_type', { type: type});
    // Redirect to main.html
    window.location.href = '/main';
}