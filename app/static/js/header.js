
document.addEventListener('DOMContentLoaded', () => {
  checkSignIn();
  getNotifications();
});

function showUserInterface(isSignedIn) {
  const signInBtn = document.getElementById('sign-in-btn');
  const signUpBtn = document.getElementById('sign-up-btn');
  const signOutBtn = document.getElementById('sign-out-btn');
  const usersBtn = document.getElementById('users-btn');
  const myDBABtn = document.getElementById('myDBA-btn');
  const casesBtn = document.getElementById('cases-btn');
  const driveImageBtn = document.getElementById('drive-image');
  const providersBtn = document.getElementById('providers');
  const notification = document.getElementById('notifications');

  if (isSignedIn) {
    signInBtn.style.display = 'none';
    signUpBtn.style.display = 'none';
    signOutBtn.style.display = 'inline-block';
    casesBtn.style.display = 'inline-block';
    notification.style.display = 'inline-block';
    if (usersBtn) {
      usersBtn.style.display = 'inline-block';
    }
    if (myDBABtn) {
      myDBABtn.style.display = 'inline-block';
    }
    if (driveImageBtn) {
      driveImageBtn.style.display = 'inline-block';
    }
    if (providersBtn) {
      providersBtn.style.display = 'inline-block';
    }
  } else {
    signInBtn.style.display = 'inline-block';
    signUpBtn.style.display = 'inline-block';
    signOutBtn.style.display = 'none';
    notification.style.display = 'none';
    if (usersBtn) {
      usersBtn.style.display = 'none';
    }
    if (myDBABtn) {
      myDBABtn.style.display = 'none';
    }
    casesBtn.style.display = 'none';
    if (driveImageBtn) {
      driveImageBtn.style.display = 'none';
    }
    if (providersBtn) {
      providersBtn.style.display = 'none';
    }
  }
  signOutBtn.addEventListener('click', signOut);
}

async function checkSignIn() {
  showUserInterface(await validateToken());
}

async function validateToken() {
  try {
    const response = await fetch('/auth/validate-token', {
      method: 'GET',
      credentials: 'include',
    });

    if (response.ok) {
      const result = await response.json();
      return true; // Returns true if the token is valid, false otherwise
    } else {
      return false;
    }
  } catch (error) {
    console.error('Error validating token:', error);
    return false;
  }
}

function toggleMenu() {
  const navLinks = document.querySelector('.nav-links');
  navLinks.classList.toggle('active');
}

function signOut() {
  fetch('/auth/logout', {
    method: 'POST',
    credentials: 'include',
  })
    .then(() => {
      window.location.href = "/";
      checkSignIn();
    })
    .catch(err => console.error('Error logging out:', err));
}


function toggleNotificationDropdown() {
  const dropdown = document.getElementById('notification-dropdown');
  dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}


function getNotifications() {
  fetch('/notification', {
    method: 'GET',
    credentials: 'include',
  })
    .then((response) => response.json())
    .then((notifications) => {
      if (!notifications.msg) {
        // Count unread notifications
        const unreadNotifications = notifications.filter((notification) => !notification.is_read);

        // Update the notification count
        const notification_count = document.getElementById('notification-count');
        notification_count.textContent = unreadNotifications.length;

        // Populate the dropdown with notifications
        const dropdown = document.querySelector("#notification-dropdown ul");
        dropdown.innerHTML = ''; // Clear previous notifications
        notifications.forEach((notification) => {
          const notificationItem = document.createElement("li");

          // Style unread notifications differently
          if (!notification.is_read) {
            notificationItem.style.fontWeight = "bold";
          }

          const notificationLink = document.createElement("a");
          notificationLink.href = notification.action_url;
          notificationLink.textContent = notification.message;
          notificationLink.style.fontSize = "12px";

          const title = document.createElement("h3");
          title.innerHTML = notification.title;

          // Add a click event listener to the link
          notificationLink.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default link behavior
            markNotificationAsRead(notification.id, notification.action_url, notificationItem);
          });

          notificationItem.appendChild(title);
          notificationItem.appendChild(notificationLink);
          dropdown.appendChild(notificationItem);
        });

      }
    })
    .catch((err) => console.error('Error:', err));
}

// Function to mark a notification as read
function markNotificationAsRead(notificationId, actionUrl, notificationItem) {
  fetch(`/notification/${notificationId}/mark-read`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => {
      if (response.ok) {
        // Update the UI: Mark the notification as read
        notificationItem.style.fontWeight = 'normal';

        // Redirect to the action URL
        window.location.href = actionUrl;
      } else {
        throw new Error('Failed to mark notification as read');
      }
    })
    .catch((err) => console.error('Error:', err));
}
