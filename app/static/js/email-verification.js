

document.getElementById("verify-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const code = document.getElementById("code").value;

  try {
      const response = await fetch("/auth/verify-code", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, code }),
      });

      const result = await response.json();

      if (!response.ok) {
        Swal.fire({
            title: 'Failed!',
            text: (result.detail || "Unexpected error"),
            icon: 'error',
            confirmButtonText: 'Close'
          });
      } else {
        Swal.fire({
            title: 'Success!',
            text: result.message,
            icon: 'success',
            confirmButtonText: 'OK',
            timer: 2000,
          }).then(()=>{

              window.location.href = "/auth/signin/page";
          });
      }
  } catch (error) {
    Swal.fire({
        title: 'Failed!',
        text: "An unexpected error occurred. Please try again.",
        icon: 'error',
        confirmButtonText: 'Close'
      });
      console.error("Error:", error);
  }
});

function resendVerificationCode() {
    const email = new URLSearchParams(window.location.search).get('email');
    
    if (!email) {
        Swal.fire({
            title: 'Failed!',
            text: "Email is missing.",
            icon: 'error',
            confirmButtonText: 'Close'
          });
        return;
    }

    fetch("/auth/send-verification-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
    })
    .then(response => response.json())
    .then(result => {
        Swal.fire({
            title: 'Success!',
            text: result.message || result.detail || "Verification code sent.",
            icon: 'success',
            confirmButtonText: 'OK',
            timer: 2000,
          });
    })
    .catch(error => {
        Swal.fire({
            title: 'Failed!',
            text: "Error resending the verification code. Please try again.",
            icon: 'error',
            confirmButtonText: 'Close'
          });
    });
}
