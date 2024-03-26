document.addEventListener("DOMContentLoaded", () => {
    const signupForm = document.getElementById("signupForm");

    signupForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way

        const formData = new FormData(signupForm);
        const data = Object.fromEntries(formData.entries());

        fetch("/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (response.ok) {
                alert("Signup successful!");
                window.location.href = "/login"; // Redirect to the login page
            } else {
                response.json().then(data => {
                    if (data.error) {
                        alert(data.error); // Show error message from the server
                    }
                });
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
