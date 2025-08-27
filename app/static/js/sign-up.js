// Handle Sign Up Form Submission
document.getElementById("signUpForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission behavior

    // Gather form data
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    // Send the form data to the server via Fetch API
    fetch("/auth/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(async (result) => {
            if (result.message) {
                // If sign-up is successful, send a verification code to the provided email
                const email = document.getElementById("email").value;
                const role = data.role;
                try {
                    const response = await fetch("/auth/send-verification-code", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ email, role }),
                    });

                    const verificationResult = await response.json();
                    Swal.fire({
                        title: 'Success!',
                        text: verificationResult.message || verificationResult.detail,
                        icon: 'success',
                        confirmButtonText: 'OK',
                        timer: 3000,
                        timerProgressBar: true
                    }).then(() => {
                        if (data.role === "institution") {
                            window.location.href = `/`;
                        } else {
                            window.location.href = `/auth/verification-page?email=${email}`;
                        }
                    });

                } catch (error) {
                    Swal.fire({
                        title: 'Failed!',
                        text: "Error sending verification code. Please try again.",
                        icon: 'error',
                        confirmButtonText: 'Close'
                    });
                }
            } else if (result.error) {
                // Display error message if something went wrong
                Swal.fire({
                    title: 'Failed!',
                    text: `Error: ${result.error}`,
                    icon: 'error',
                    confirmButtonText: 'Close'
                });
            }
        })
        .catch(error => {
            Swal.fire({
                title: 'Failed!',
                text: "An error occurred while processing your request.",
                icon: 'error',
                confirmButtonText: 'Close'
            });
        });
});

// Optional: Handle Google Sign-Up Button Click (it will navigate to Google sign-up flow)
document.getElementById("googleSignUpBtn").addEventListener("click", function () {
    window.location.href = '/auth/google/login'; // Redirect to Google sign-in page
});


const userBtn = document.getElementById("userBtn");
const institutionBtn = document.getElementById("institutionBtn");
document.getElementById("userBtn").addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("name").placeholder = "Enter your name";
    document.getElementById("email").placeholder = "Enter your email";
    document.getElementById("role").value = "user";
    this.classList.add("active");
    document.getElementById("institutionBtn").classList.remove("active");
});

document.getElementById("institutionBtn").addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("name").placeholder = "Enter your institution name";
    document.getElementById("email").placeholder = "Enter your institution email";
    document.getElementById("role").value = "institution";
    this.classList.add("active");
    document.getElementById("userBtn").classList.remove("active");
});
