const provider_id = document.getElementById("provider_id").value;
fetchCases();
document.addEventListener("DOMContentLoaded", () => {
    const uploadDateInput = document.getElementById("uploadDate");
    const today = new Date().toISOString().split("T")[0];
    uploadDateInput.value = today;
});

const modal = document.getElementById("addCaseModal");


window.onclick = (event) => {
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

document.getElementById("addCaseBtn").addEventListener("click", () => {
    document.getElementById("addCaseModal").style.display = "flex";
});
document.getElementById("addCaseForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    try {
        const fetchResponse = await fetch(`/case?provider_id=${provider_id}`, {
            method: "POST",
            credentials: 'include',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        const responseData = await fetchResponse.json();

        if (!fetchResponse.ok) {
            const errorMessage = responseData.detail || JSON.stringify(responseData);
            Swal.fire({
                title: 'Failed!',
                text: `Failed to add case:${errorMessage}`,
                icon: 'error',
                confirmButtonText: 'Close'
            });
            return;
        }

        document.getElementById("addCaseModal").style.display = "none";
        fetchCases();
    } catch (error) {
        console.error("Error:", error);
        Swal.fire({
            title: 'Failed!',
            text: `An unexpected error occurred:${error.message || error}`,
            icon: 'error',
            confirmButtonText: 'Close'
        });
    }
});

function fetchCases() {
    const loadingIndicator = document.getElementById("loadingIndicator");
    loadingIndicator.style.display = "block";
    fetch(`/case/?provider_id=${provider_id}`, {
        method: "GET",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json"
        }
    }).then((response) => response.json())
        .then((cases) => {
            loadingIndicator.style.display = "none";
            const tbody = document.querySelector("#casesTable tbody");
            tbody.innerHTML = "";
            cases.forEach((caseItem) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${caseItem.id}</td>
                    <td>${caseItem.name}</td>
                    <td>${caseItem.create_date_without_time}</td>
                    <td>${caseItem.creator.name}</td>
                    <td>${caseItem.owner.name}</td>
                    <td>${caseItem.comments}</td>
                    <td>
                        <button class="styled-button" onclick="detailsPage(${caseItem.id})">Details</button>
                        <button class="styled-button" onclick="openEditModal(${caseItem.id}, '${caseItem.name}', '${caseItem.create_date_without_time}','${caseItem.comments}','${caseItem.creator.email}','${caseItem.owner.email}')">Edit</button>
                        <button class="styled-button" onclick="deleteCase(${caseItem.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }).catch((error) => {
            loadingIndicator.style.display = "none";
            console.error('Error:', error);
        });
}

function openEditModal(id, name, create_date, comments, provider, owner) {
    document.getElementById("editModal").style.display = "flex";

    document.getElementById("editCaseId").value = id;
    document.getElementById("editName").value = name;
    document.getElementById("editUploadDate").value = create_date;
    document.getElementById("editComments").value = comments;
    document.getElementById("editProvider").value = provider;
    document.getElementById("editOwner").value = owner;
}

function deleteCase(id) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/case/${id}`, {
                method: "DELETE",
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(() => {
                fetchCases();
                Swal.fire(
                    'Deleted!',
                    'The Case has been deleted.',
                    'success'
                );
            }).catch(error => {
                console.error('Error:', error);
                Swal.fire(
                    'Error!',
                    'There was an issue deleting the Case.',
                    'error'
                );
            });
        } else {
            console.log('Case deletion canceled');
        }
    });
}

window.addEventListener("click", (event) => {
    if (event.target === document.getElementById("editModal")) {
        document.getElementById("editModal").style.display = "none";
    }
});

document.getElementById("editCaseForm").addEventListener("submit", (event) => {

    event.preventDefault();
    const id = document.getElementById("editCaseId").value;
    const name = document.getElementById("editName").value;
    const create_date = document.getElementById("editUploadDate").value;
    const comments = document.getElementById("editComments").value;
    const owner = document.getElementById("editOwner").value;
    const provider = document.getElementById("editProvider").value;
    fetch(`/case/${id}`, {
        method: "PUT",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, create_date, comments, provider, owner }),
    })
        .then((response) => response.json())
        .then((res) => {
            if (res.status === 200) {
                Swal.fire({
                    title: 'Success!',
                    icon: 'success',
                    text: "Data Updated!",
                    confirmButtonText: 'OK',
                    timer: 3000,
                    timerProgressBar: true
                }).then(() => {
                    document.getElementById("editModal").style.display = "none";
                    fetchCases();
                });
            } else {
                Swal.fire(
                    'Error!',
                    `${res.error}`,
                    'error'
                );
            }
        });
});

function detailsPage(case_id) {
    window.location.href = `/case/page/${case_id}?provider_id=${provider_id}`;
}
