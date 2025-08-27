fetchUsers();
// Fetch and display users

function fetchUsers() {
    // Show the loading indicator
    const loadingIndicator = document.getElementById("loadingIndicator");
    loadingIndicator.style.display = "block";
    fetch("/user", {
        method: "GET",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => response.json())
        .then((users) => {
            // Hide the loading indicator when data is fetched
            loadingIndicator.style.display = "none";

            const tbody = document.querySelector("#userTable tbody");
            tbody.innerHTML = "";
            users.forEach((user) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${user.id}</td>
                    <td>${user.name}</td>
                    <td>${user.email}</td>
                    <td>${user.password}</td>
                    <td>${user.role}</td>
                    <td>${user.is_verified}</td>
                    <td>
                        <button class="styled-button" onclick="openEditModal(${user.id}, '${user.name}', '${user.email}','${user.password}', '${user.role}', '${user.is_verified}')">Edit</button>
                        <button class="styled-button" onclick="deleteUser(${user.id})">Delete</button>
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


function openEditModal(id, name, email, password, role, is_verified) {
    // Display the modal
    document.getElementById("editModal").style.display = "flex";

    // Set form values
    document.getElementById("editUserId").value = id;
    document.getElementById("editName").value = name;
    document.getElementById("editUserEmail").value = email;
    document.getElementById("editUserPassword").value = password;
    document.getElementById("editRole").value = role;
    document.getElementById("is_verified").value = is_verified;
}

document.getElementById("editUserForm").addEventListener("submit", (event) => {

    event.preventDefault();
    const id = document.getElementById("editUserId").value;
    const name = document.getElementById("editName").value;
    const email = document.getElementById("editUserEmail").value;
    const password = document.getElementById("editUserPassword").value;
    const role = document.getElementById("editRole").value;
    const is_verified = document.getElementById("is_verified").value;
    fetch(`/user/${id}`, {
        method: "PUT",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email, password, role, is_verified }),
    })
        .then((response) => response.json())
        .then(() => {
            document.getElementById("editModal").style.display = "none";
            fetchUsers();
        });
});

function deleteUser(id) {
    // Use SweetAlert to ask for confirmation
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/user/${id}`, {
                method: "DELETE",
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then((res) => {
                if (res.status === 200) {
                    fetchUsers();
                    Swal.fire(
                        'Deleted!',
                        'The user has been deleted.',
                        'success'
                    );
                } else {
                    Swal.fire(
                        'Error!',
                        'There was an issue deleting the user.',
                        'error'
                    );
                }
            }).catch(error => {
                console.error('Error:', error);
                Swal.fire(
                    'Error!',
                    'There was an issue deleting the user.',
                    'error'
                );
            });
        } else {
            console.log('User deletion canceled');
        }
    });
}


// Close modal on outside click
window.addEventListener("click", (event) => {
    if (event.target === document.getElementById("editModal")) {
        document.getElementById("editModal").style.display = "none";
    }
});


// Open Add User Modal
document.getElementById("addUserBtn").addEventListener("click", () => {
    document.getElementById("addUserModal").style.display = "flex";
});

// Add User Form Submission
document.getElementById("addUserForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    fetch("/user", {
        method: "POST",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((res) => {
            console.log(res)
            if (res.errors) {
                let msg = "";

                for (let error of res.errors) {
                    msg += error.msg + "\n";
                }

                Swal.fire(
                    'Error!',
                    msg,
                    'error'
                );
            } else {
                document.getElementById("addUserModal").style.display = "none";
                fetchUsers();
            }

        }).catch(error => {
            console.error('Error:', error);
            Swal.fire(
                'Error!',
                error,
                'error'
            );
        });
});

// Close modal on outside click
window.addEventListener("click", (event) => {
    if (event.target === document.getElementById("addUserModal")) {
        document.getElementById("addUserModal").style.display = "none";
    }
});
