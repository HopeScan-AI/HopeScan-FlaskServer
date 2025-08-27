document.getElementById("signInForm").addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
        // Send the form data to the server via fetch API
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (!response.ok) {
            Swal.fire({
                title: 'Failed!',
                text: "Login failed: " + (result.error || "Unexpected error"),
                icon: 'error',
                confirmButtonText: 'Close'
            });
        } else {
            window.location.href = `/?role=${result.user.role}`;
        }
    } catch (error) {
        console.error("Error:", error);
        Swal.fire({
            title: 'Failed!',
            text: "An unexpected error occurred. Please try again.",
            icon: 'error',
            confirmButtonText: 'Close'
        });
    }
});
