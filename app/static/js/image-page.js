document.getElementById("uploadForm").addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the default form submission
    
    const formData = new FormData(event.target);
    const token = getAuthToken();  // Replace with your actual token (e.g., from localStorage, a cookie, or a variable)
    const caseId = formData.get("case_id");
    formData.append("diagnose", document.getElementById("diagnose").value);
    formData.append("comments", document.getElementById("comments").value);

    try {
        // Send the form data and token to the server using the fetch API
        const response = await fetch(`/images/upload/${caseId}`, {
            method: "POST",
            credentials: 'include',
            body: formData,
        });

        if (response.ok) {
            Swal.fire({
                title: 'Success!',
                text: 'Image uploaded successfully!',
                icon: 'success',
                confirmButtonText: 'OK',
                timer: 2000,
                timerProgressBar: true
              }).then(() => {
                window.location.href = `/case/page/${caseId}`;
              });
        } else {
            const error = await response.json();
            Swal.fire({
                title: 'Error!',
                text: (error.message || "An unexpected error occurred"),
                icon: 'error',
                confirmButtonText: 'Close'
              });
        }
    } catch (error) {
        console.error("Error:", error);
        Swal.fire({
            title: 'Error!',
            text: "An unexpected error occurred. Please try again.",
            icon: 'error',
            confirmButtonText: 'Close'
          });
    }
});

function getAuthToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim(); 
      if (cookie.startsWith('access_token=')) {
        return cookie.split('=')[1];
      }
    }
  
    return localStorage.getItem('access_token');
  }

  