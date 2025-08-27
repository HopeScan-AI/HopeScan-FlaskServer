let currentPage = 1;
const limit = 10;
const resultsTableBody = document.querySelector("#results-table tbody");
const pageNum = document.getElementById("page-num");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");
const showAllBtn = document.getElementById("show-all");
let is_filtered = false;


async function fetchResults(page) {
    const loadingIndicator = document.getElementById("loadingIndicator");
    loadingIndicator.style.display = "block";
    resultsTableBody.innerHTML = '';
    const response = await fetch(`/drive-images/results/data?page=${page}&limit=${limit}`);
    loadingIndicator.style.display = "none";
    const data = await response.json();
    const pages = data.pages;
    // Clear the current table rows

    // Populate the table with new data
    data.data.forEach(result => {
        const row = document.createElement('tr');

        row.innerHTML = `
                <td>${result.name}</td>
                <td>${result.old_diagnose || 'N/A'}</td>
                <td>${result.doctore_diagnose.filter(d => d.diagnose === "normal").length}</td>
                <td>${result.doctore_diagnose.filter(d => d.diagnose === "benign").length}</td>
                <td>${result.doctore_diagnose.filter(d => d.diagnose === "malignant").length}</td>
                <td>${result.doctore_diagnose.filter(d => d.diagnose === "discard").length}</td>
            `;

        row.addEventListener('click', () => openModal(result));

        resultsTableBody.appendChild(row);
    });




    document.getElementById('closeModal').addEventListener('click', () => {
        document.getElementById('customModal').style.display = 'none';
    });

    window.onclick = (event) => {
        const modal = document.getElementById('customModal');
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };


    // Update the current page number
    pageNum.textContent = `${currentPage} of ${pages}`;

    // Enable or disable pagination buttons
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = data.length < limit;
}


function openModal(result) {
    // Set modal header content
    document.getElementById('modalName').textContent = result.name;
    document.getElementById('modalOldDiagnose').textContent = result.old_diagnose || 'N/A';

    // Populate the modal table body
    const modalTableBody = document.querySelector("#modal-table tbody");
    modalTableBody.innerHTML = '';

    result.doctore_diagnose.forEach(diagnose => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${diagnose.user}</td>
            <td>${diagnose.diagnose === "normal" ? "&#10004;" : ''}</td>
            <td>${diagnose.diagnose === "benign" ? "&#10004;" : ''}</td>
            <td>${diagnose.diagnose === "malignant" ? "&#10004;" : ''}</td>
            <td>${diagnose.diagnose === "discard" ? "&#10004;" : ''}</td>
        `;

        modalTableBody.appendChild(row);
    });

    // Show the modal
    document.getElementById('customModal').style.display = 'block';
}

prevBtn.addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        if (is_filtered) {
            fetch_filtered(currentPage);
        } else {
            fetchResults(currentPage);
        }
    }
});

nextBtn.addEventListener("click", () => {
    currentPage++;
    if (is_filtered) {
        fetch_filtered(currentPage);
    } else {
        fetchResults(currentPage);
    }
});

showAllBtn.addEventListener("click", () => {
    is_filtered = false;
    currentPage = 1;
    fetchResults(currentPage);
});


// Initial fetch
fetchResults(currentPage);

const filterButton = document.getElementById("filter-different");

filterButton.addEventListener("click", () => {
    is_filtered = true;
    currentPage = 1;
    fetch_filtered(currentPage);
})


async function fetch_filtered(page) {
    try {
        const loadingIndicator = document.getElementById("loadingIndicator");
        loadingIndicator.style.display = "block";
        resultsTableBody.innerHTML = '';
        const response = await fetch(`/drive-images/different_diagnoses?page=${page}&limit=${limit}`);
        loadingIndicator.style.display = "none";
        const data = await response.json();

        // Clear the existing table rows

        // Populate the table with the filtered results
        data.forEach(result => {
            const row = document.createElement('tr');

            // Build the row HTML
            row.innerHTML = `
                <td>${result.name}</td>
                <td>${result.old_diagnose || 'N/A'}</td>
                <td>${result.doctore_diagnose.filter(d => d.diagnose === "normal").length}</td>
                <td>${result.doctore_diagnose.filter(d => d.diagnose === "benign").length}</td>
                <td>${result.doctore_diagnose.filter(d => d.diagnose === "malignant").length}</td>
                <td>${result.doctore_diagnose.filter(d => d.diagnose === "discard").length}</td>
            `;
            row.addEventListener('click', () => openModal(result));
            // Append the row to the table body
            resultsTableBody.appendChild(row);
        });
        pageNum.textContent = `${currentPage}`
        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = data.length < limit;
    } catch (error) {
        console.error("Error fetching filtered results:", error);
    }
};
