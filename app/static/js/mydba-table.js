fetchTables();
// Fetch and display tables

function fetchTables() {    
    // Show the loading indicator
    const loadingIndicator = document.getElementById("loadingIndicator");
    loadingIndicator.style.display = "block";
    var tableElement = document.getElementById("table-container");
    var tableName = tableElement.getAttribute("data-table-name");  // Get table name from HTML
    
    fetch(`/myDBA/showTable/${tableName}`, {
        method: "GET",
        credentials: 'include',
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => response.json())
        .then(data => {
            // Hide the loading indicator when data is fetched
            loadingIndicator.style.display = "none";
            if (data.error) {
                console.error("Error:", data.error);
                return;
            }

            var columns = data.columns;
            var rows = data.rows;

            var tableHeader = document.getElementById("table-header");
            var tableBody = document.getElementById("table-body");

            // Clear existing data (if any)
            tableHeader.innerHTML = "";
            tableBody.innerHTML = "";

            // Create table headers dynamically
            columns.forEach(column => {
                
                let th = document.createElement("th");
                th.textContent = column;
                tableHeader.appendChild(th);
            });
            let th = document.createElement("th");
            th.textContent = "Action";
            tableHeader.appendChild(th);

            // Create table rows dynamically
            rows.forEach(row => {
                let tr = document.createElement("tr");

                columns.forEach(column => {
                    let td = document.createElement("td");
                    td.textContent = row[column];  // Fill cell with row data
                    tr.appendChild(td);
                });

                let td = document.createElement("td");
                td.innerHTML = `<a href="/myDBA/delete/${tableName}/${row.id}">Delete</a>`;
                tr.appendChild(td);

                tableBody.appendChild(tr);
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
