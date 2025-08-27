fetchProviders();

document.getElementById("addProviderForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    fetch("/provider", {
        method: "POST",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (!response.ok) {
                if (response.status === 404) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error 404',
                        text: "There is no user with this email",
                    });
                }
                if (response.status === 400) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error 400',
                        text: `provider already exist!`,
                    });
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((res) => {
            document.getElementById("addProviderModal").style.display = "none";
            fetchProviders();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});


document.getElementById("addProviderBtn").addEventListener("click", () => {
    document.getElementById("addProviderModal").style.display = "flex";
});



function fetchProviders() {
    // Show the loading indicator
    const loadingIndicator = document.getElementById("loadingIndicator");
    loadingIndicator.style.display = "block";
    fetch("/provider", {
        method: "GET",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => response.json())
        .then((providers) => {
            // Hide the loading indicator when data is fetched
            loadingIndicator.style.display = "none";

            const tbody = document.querySelector("#providersTable tbody");
            tbody.innerHTML = "";
            providers.forEach((provider) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${provider.id}</td>
                    <td>${provider.provider.name}</td>
                    <td>${provider.provider.email}</td>
                    <td>${provider.status}</td>
                    <td>
                        <button class="styled-button" onclick="openDetails(${provider.provider.id})">Details</button>
                        <button class="styled-button" onclick="deleteProvider(${provider.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch((error) => {
            // Hide loading indicator in case of error
            loadingIndicator.style.display = "none";
            console.error('Error:', error);
        });
}

function openDetails(provider_id) {
    window.location.href = `/case/page?provider_id=${provider_id}`;
}

window.addEventListener("click", (event) => {
    if (event.target === document.getElementById("addProviderModal")) {
        document.getElementById("addProviderModal").style.display = "none";
    }
});

function deleteProvider(id) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/provider/${id}`, {
                method: "DELETE",
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(() => {
                fetchProviders();
                Swal.fire(
                    'Deleted!',
                    'The provider has been deleted.',
                    'success'
                );
            }).catch(error => {
                console.error('Error:', error);
                Swal.fire(
                    'Error!',
                    'There was an issue deleting the provider.',
                    'error'
                );
            });
        } else {
            console.log('Provider deletion canceled');
        }
    });
}
