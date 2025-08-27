const spinner = document.getElementById("spinner");
spinner.style.display = "block";

fetch(`/images/${caseId}`)
  .then((response) => response.json())
  .then((images) => {
    const container = document.getElementById('image-container');
    // Display each image
    Object.entries(images).forEach((image) => {
      if (image) {
        // Create a new div element to wrap the image and caption
        const imageWrapper = document.createElement('div');
        imageWrapper.classList.add('image-card');

        // Create the img element
        const img = document.createElement('img');
        img.src = `data:image/${image[1].file_name.split('.')[1]};base64,${image[1].image}`;
        img.alt = image[1].file_name;
        img.style = 'width: 100%; border-radius: 8px; cursor: pointer;';

        // Create a caption element
        const caption = document.createElement('p');
        caption.textContent = `Filename: ${image[1].file_name}`;
        caption.style = 'text-align: center; margin-top: 8px; font-size: 18px; color: #009688;';

        // Append the img and caption to the imageWrapper
        imageWrapper.appendChild(img);
        imageWrapper.appendChild(caption);

        // Append the imageWrapper to the container
        container.appendChild(imageWrapper);

        // Create the modal
        const modal = document.createElement('div');
        modal.classList.add('modal');
        modal.style.display = 'none';

        // Create the card structure inside the modal
        const card = document.createElement('div');
        card.classList.add('card');
        card.style = `
        background-color: #fff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        max-width: 90%;
        max-height: 90%;
        display: flex;
        flex-direction: column;
        align-items: center;
      `;

        // Create the modal image
        const modalImage = document.createElement('img');
        modalImage.src = img.src;
        modalImage.style = `
        max-width: 100%;
        max-height: 60vh; /* Ensure the image doesn't exceed 60% of the viewport height */
        object-fit: contain;
        border-radius: 8px;
        margin-bottom: 16px;
      `;

        // Create the card container for additional info
        const cardContainer = document.createElement('div');
        cardContainer.classList.add('container');

        // Add title and description
        const title = document.createElement('h4');
        title.innerHTML = `<b>${image[1].file_name}</b>`;
        const description = document.createElement('p');
        description.textContent = 'Additional details about the image can go here.';

        cardContainer.appendChild(title);
        cardContainer.style = `
      background-color: antiquewhite;
  padding: 10px;
  border-radius: 10px;
      `
        cardContainer.appendChild(description);

        card.appendChild(modalImage);
        card.appendChild(cardContainer);

        // Create the close button
        const closeButton = document.createElement('span');
        closeButton.textContent = '×';
        closeButton.classList.add('close');
        closeButton.style = `
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 30px;
        cursor: pointer;
      `;

        modal.appendChild(card);
        modal.appendChild(closeButton);

        document.body.appendChild(modal);

        // Image click handler for modal
        img.addEventListener('click', () => {
          modal.style.display = 'flex';
          modal.style.justifyContent = 'center';
          modal.style.alignItems = 'center';
        });

        // Close button click handler
        closeButton.addEventListener('click', () => {
          modal.style.display = 'none'; // Hide the modal
        });

        // Close modal when clicking outside the card
        modal.addEventListener('click', (event) => {
          if (event.target === modal) {
            modal.style.display = 'none'; // Hide the modal
          }
        });
      }
    });
  }).then(() => {
    spinner.style.display = 'none';
  })
  .catch((error) => console.error('Error fetching images:', error));



document.getElementById("change-owner").addEventListener("click", (event) => {
  document.getElementById("change-owner-modal").style.display = "flex";
});

window.addEventListener("click", (event) => {
  if (event.target === document.getElementById("change-owner-modal")) {
    document.getElementById("change-owner-modal").style.display = "none";
  }
});


document.getElementById("newOwnerForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData.entries());
  fetch("/case/change-owner", {
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
      if (res.status === 200) {
        Swal.fire({
          title: 'Success!',
          icon: 'success',
          text: "Owner Changed!",
          confirmButtonText: 'OK',
          timer: 3000,
          timerProgressBar: true
        }).then(() => {
          window.location.href = "/case/page";
        });
      } else {
        Swal.fire(
          'Error!',
          `${res.error}`,
          'error'
        );
      }
    }).catch((error) => console.error('Error change owner:', error));
});