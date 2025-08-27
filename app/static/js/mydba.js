fetchTables();
// Fetch and display tables

function fetchTables() {
    // Show the loading indicator
    const loadingIndicator = document.getElementById("loadingIndicator");
    loadingIndicator.style.display = "block";
    fetch("/myDBA", {
        method: "GET",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => response.json())
        .then((tables) => {
            // Hide the loading indicator when data is fetched
            loadingIndicator.style.display = "none";
            
            const tbody = document.querySelector("#tablesTable");
            tbody.innerHTML = "";
            tables.forEach((table) => {
                tbody.innerHTML += `<h3>${table.table_name} <a href="/myDBA/show/${table.table_name}">Show</a> <a href="/myDBA/delete/${table.table_name}">Empty</a> <a href="/myDBA/export/${table.table_name}">Export</a></h3>`;
                const tableHTML = document.createElement("table");
                const row = document.createElement("tr");
                row.innerHTML = ``;
                table.columns.forEach((column) => {
                row.innerHTML += `<th>${column.name}</th>`;
                });
                row.innerHTML += `
                    <!--<th>
                        <button class="styled-button" onclick="openEditModal(${table.id}, '${table.name}', '${table.email}', '${table.role}', '${table.is_verified}')">Edit</button>
                        <button class="styled-button" onclick="deletetable(${table.id})">Delete</button>
                    </th>-->
                `;
                tableHTML.appendChild(row);
                tbody.appendChild(tableHTML);
                //const row1 = document.createElement("tr");
                //tbody.appendChild(row1);
            });
        })
        .catch((error) => {
            // Hide loading indicator in case of error
            loadingIndicator.style.display = "none";
            console.error('Error:', error);
        });
}


function openEditModal(id, name, email, role, is_verified) {
    // Display the modal
    document.getElementById("editModal").style.display = "flex";
    
    // Set form values
    document.getElementById("edittableId").value = id;
    document.getElementById("editName").value = name;
    document.getElementById("edittableEmail").value = email;
    document.getElementById("editRole").value = role;
    document.getElementById("is_verified").value = is_verified;
}

document.getElementById("edittableForm").addEventListener("submit", (event) => {
    
    event.preventDefault();
    const id = document.getElementById("edittableId").value;
    const name = document.getElementById("editName").value;
    const email = document.getElementById("edittableEmail").value;
    const role = document.getElementById("editRole").value;
    const is_verified = document.getElementById("is_verified").value;
    fetch(`/table/${id}`, {
        method: "PUT",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email, role, is_verified }),
    })
        .then((response) => response.json())
        .then(() => {
            document.getElementById("editModal").style.display = "none";
            fetchTables();
        });
});

function deletetable(id) {
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
            fetch(`/table/${id}`, { 
                method: "DELETE",
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            }).then(() => {
                fetchTables();
                Swal.fire(
                    'Deleted!',
                    'The table has been deleted.',
                    'success'
                );
            }).catch(error => {
                console.error('Error:', error);
                Swal.fire(
                    'Error!',
                    'There was an issue deleting the table.',
                    'error'
                );
            });
        } else {
            // table canceled the deletion
            console.log('table deletion canceled');
        }
    });
}


// Close modal on outside click
window.addEventListener("click", (event) => {
    if (event.target === document.getElementById("editModal")) {
        document.getElementById("editModal").style.display = "none";
    }
});


// Open Add table Modal
document.getElementById("addtableBtn").addEventListener("click", () => {
    document.getElementById("addtableModal").style.display = "flex";
});

// Add table Form Submission
document.getElementById("addtableForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    fetch("/table", {
        method: "POST",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((res) => {
            document.getElementById("addtableModal").style.display = "none";
            fetchTables(); // Refresh the table list
        });
});

// Close modal on outside click
window.addEventListener("click", (event) => {
    if (event.target === document.getElementById("addtableModal")) {
        document.getElementById("addtableModal").style.display = "none";
    }
});

document.getElementById("importForm").addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the default form submission
    
    const formData = new FormData(event.target);
    const token = getAuthToken();  // Replace with your actual token (e.g., from localStorage, a cookie, or a variable)
    try {
        // Send the form data and token to the server using the fetch API
        const response = await fetch(`/myDBA/import`, {
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
                window.location.href = `/myDBA/page`;
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
