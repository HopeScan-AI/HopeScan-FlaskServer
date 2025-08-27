
const imagesPerPage = 3; 
let currentPage = 1; 
let totalImages = 0; 
let totalPages = 0; 

async function fetchWithAuth(url, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...options.headers,
    };

    const response = await fetch(url, { ...options, headers });
    if (!response.ok) {
        Swal.fire({
            title: 'Failed!',
            text: `Error: ${response.statusText}`,
            icon: 'error',
            confirmButtonText: 'Close'
          });
        throw new Error(response.statusText);
    }
    return response.json();
}


async function fetchImages() {
    const skip = (currentPage - 1) * imagesPerPage;
    const limit = imagesPerPage;
    const data = await fetchWithAuth(`/drive-images/get?skip=${skip}&limit=${limit}`, { credentials: 'include' });
    totalImages = data.total; 
    totalPages = Math.ceil(totalImages / imagesPerPage);
    renderImagesGrid(data); 
    renderPagination("all");
}


async function fetchImagesWithoutDiagnose() {
    const skip = 0;
    const limit = 3;
    const data = await fetchWithAuth(`/drive-images/get_no_diagnose?skip=${skip}&limit=${limit}`, { credentials: 'include' });
    totalImages = data.total; 
    totalPages = Math.ceil(totalImages / imagesPerPage);
    renderImagesGrid(data); 
    renderPagination("WithoutDiagnose");
}


function renderImagesGrid(images) {
    const gridContainer = document.getElementById('images-table');
    gridContainer.innerHTML = "";
    images.forEach(image => {
        const imageCard = document.createElement("div");
        imageCard.classList.add("image-card");
        imageCard.style.width = "400px"; 
        imageCard.style.margin = "10px";
        imageCard.style.padding = "10px"; 
        imageCard.style.backgroundColor = "#ffffff";
        imageCard.style.border = "1px solid #ddd";
        imageCard.style.borderRadius = "12px"; 
        imageCard.style.boxShadow = "0 6px 10px rgba(0, 0, 0, 0.15)"; 
        imageCard.style.display = "flex";
        imageCard.style.flexDirection = "column";
        imageCard.style.alignItems = "center";

        
        const iframe = document.createElement("iframe");
        iframe.src = `https://drive.google.com/file/d/${image.image_id}/preview`;
        iframe.alt = image.name;
        iframe.style.border = "none";
        iframe.style.width = "100%";
        iframe.style.height = "450px"; 
        iframe.style.borderRadius = "10px";

        
        const radioContainer = document.createElement("div");
        radioContainer.classList.add("radio-container");
        radioContainer.style.marginTop = "20px"; 
        radioContainer.style.display = "flex";
        radioContainer.style.justifyContent = "space-between"; 
        radioContainer.style.gap = "20px"; 
        radioContainer.style.padding = "10px"; 
        radioContainer.style.backgroundColor = "#f9f9f9";
        radioContainer.style.border = "1px solid #ddd";
        radioContainer.style.borderRadius = "10px";
        radioContainer.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";

        
        const options = [
            { label: " Normal", value: "normal" },
            { label: " Benign", value: "benign" },
            { label: " Malignant", value: "malignant" },
            { label: " Discard", value: "discard" }
        ];

        options.forEach(option => {
            
            const label = document.createElement("label");

            
            const radioInput = document.createElement("input");
            radioInput.type = "radio";
            radioInput.name = `image-${image.image_id}`; 
            radioInput.value = option.value;

            if (image.diagnose && image.diagnose === option.value) {
                radioInput.checked = true;
            }

            
            radioInput.addEventListener("change", () => {
                sendToBackend(image.image_id, radioInput.value);
            });

            
            label.appendChild(radioInput);
            label.appendChild(document.createTextNode(option.label));

            
            radioContainer.appendChild(label);
        });

        
        imageCard.appendChild(iframe);
        imageCard.appendChild(radioContainer);
        gridContainer.appendChild(imageCard);
    });

    
    gridContainer.style.display = "flex";
    gridContainer.style.flexWrap = "wrap";
    gridContainer.style.justifyContent = "center";
    gridContainer.style.gap = "25px"; 
}



function sendToBackend(imageId, value) { 
    fetch('/drive-images/create-doctor-diagnose', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image_drive_id: imageId, diagnose: value }),
    })
        .then(response => {
            if (response.ok) {
                console.log(`Image ${imageId} status updated to: ${value}`);
            } else {
                Swal.fire({
                    title: 'Failed!',
                    text: `Failed to update image ${imageId} status`,
                    icon: 'error',
                    confirmButtonText: 'Close'
                  });
                
            }
        })
        .catch(error => console.error('Error:', error));
}




function renderPagination(images_type) {
    const paginationContainerTop = document.getElementById("paginationTop");
    const paginationContainerDown = document.getElementById("paginationDown");
    paginationContainerTop.innerHTML = "";
    paginationContainerDown.innerHTML = ""; 
    paginationContainerTop.style.display = "flex";
    paginationContainerDown.style.display = "flex";
    paginationContainerTop.style.justifyContent = "center";
    paginationContainerDown.style.justifyContent = "center";
    paginationContainerTop.style.gap = "10px";
    paginationContainerDown.style.gap = "10px";
    paginationContainerTop.style.marginTop = "20px";
    paginationContainerDown.style.marginTop = "20px";

    
    const createButton = (text, disabled, onClick) => {
        const button = document.createElement("button");
        button.innerText = text;
        button.disabled = disabled;
        button.onclick = onClick;
        button.style.padding = "10px 15px";
        button.style.border = "1px solid #ddd";
        button.style.borderRadius = "8px";
        button.style.backgroundColor = disabled ? "#f0f0f0" : "#009688";
        button.style.color = disabled ? "#aaa" : "#fff";
        button.style.cursor = disabled ? "not-allowed" : "pointer";
        button.style.transition = "background-color 0.3s ease, transform 0.2s ease";

        button.addEventListener("mouseover", () => {
            if (!disabled) {
                button.style.backgroundColor = "#009688";
                button.style.transform = "scale(1.05)";
            }
        });

        button.addEventListener("mouseout", () => {
            if (!disabled) {
                button.style.backgroundColor = "#009688";
                button.style.transform = "scale(1)";
            }
        });

        return button;
    };

    
    const prevButtonTop = createButton("Previous", currentPage === 1, () => changePage(currentPage - 1, images_type));
    const prevButtonDown = createButton("Previous", currentPage === 1, () => changePage(currentPage - 1, images_type));
    paginationContainerTop.appendChild(prevButtonTop);
    paginationContainerDown.appendChild(prevButtonDown);

    
    for (let i = 1; i <= totalPages; i++) {
        const pageButtonTop = createButton(i, i === currentPage, () => changePage(i, images_type));
        const pageButtonDown = createButton(i, i === currentPage, () => changePage(i, images_type));
        if (i === currentPage) {
            pageButtonTop.style.backgroundColor = "#009688";
            pageButtonDown.style.backgroundColor = "#009688";
            pageButtonTop.style.cursor = "default";
            pageButtonDown.style.cursor = "default";
        }
        paginationContainerTop.appendChild(pageButtonTop);
        paginationContainerDown.appendChild(pageButtonDown);
    }

    
    const nextButtonTop = createButton("Next", currentPage === totalPages, () => changePage(currentPage + 1, images_type));
    const nextButtonDown = createButton("Next", currentPage === totalPages, () => changePage(currentPage + 1, images_type));
    paginationContainerTop.appendChild(nextButtonTop);
    paginationContainerDown.appendChild(nextButtonDown);
}



function changePage(page, images_type) {
    currentPage = page;
    if (images_type === "all"){
        fetchImages();
    }else if(images_type === "WithoutDiagnose"){
        fetchImagesWithoutDiagnose();
    }
}

function openResults(){
    window.location.href="/drive-images/results";
}

async function updateImages() {
    Swal.fire({
        title: 'Updating...',
        text: 'Please wait while we update the images.',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        },
    });

    try {
        const data = await fetchWithAuth(`/drive-images/update_content`, { credentials: 'include' });

        Swal.fire({
            title: 'Success!',
            text: data.status,
            icon: 'success',
            confirmButtonText: 'OK',
            timer: 2000,
        });
    } catch (error) {
        Swal.fire({
            title: 'Error!',
            text: 'Failed to update images. Please try again.',
            icon: 'error',
            confirmButtonText: 'OK',
        });
    }
}
