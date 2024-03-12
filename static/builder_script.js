//BUILDER.HTML
function toggleOptions() {
    var options = document.getElementById("options");
    options.classList.toggle("hidden");
}

function redirectToMain(type) {
    // Redirect to main.html with the type as a query parameter
    window.location.href = '/main?type=' + type;
}