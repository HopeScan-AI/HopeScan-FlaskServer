
document.addEventListener('DOMContentLoaded', function() {
  const lazyImages = document.querySelectorAll('.lazy-load');

  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const image = entry.target;
        image.src = image.getAttribute('data-src');
        image.classList.add('visible');
        observer.unobserve(image);
      }
    });
  }, { threshold: 0.1 });

  lazyImages.forEach(image => {
    imageObserver.observe(image);
  });

  document.getElementById('contact-form').addEventListener('submit', function(event) {
      event.preventDefault();
  
      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
      const message = document.getElementById('message').value;
  
      if (!name || !email || !message) {
        Swal.fire({
          title: 'Failed!',
          text: 'Please fill in all fields.',
          icon: 'error',
          confirmButtonText: 'Close'
        });
        return;
      }
      Swal.fire({
        title: 'Success!',
        text: 'Your message has been sent successfully!',
        icon: 'success',
        confirmButtonText: 'OK',
        timer: 2000,
        timerProgressBar: true
      });
  });
  
  const slider = document.querySelector('.hero-slider');
  const slides = document.querySelectorAll('.slide');
  let currentSlide = 0;
  
  function nextSlide() {
    slides[currentSlide].classList.remove('active');
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].classList.add('active');
    updateSliderPosition();
  }
  
  // Function to update the slider position based on the current slide
  function updateSliderPosition() {
    slider.style.transform = `translateX(-${currentSlide * 100}%)`;
  }
  
//   // Auto slide every 3 seconds
  setInterval(nextSlide, 10000);  // 3000ms = 3 seconds
});

document.addEventListener('DOMContentLoaded', function() {
  // Lazy loading for images and sections
  const lazyImages = document.querySelectorAll('.lazy-load');
  const lazySections = document.querySelectorAll('.lazy-load-section');

  // Intersection Observer for Images
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const image = entry.target;
        image.src = image.getAttribute('data-src');
        image.classList.add('visible');
        observer.unobserve(image);
      }
    });
  }, { threshold: 0.1 });

  lazyImages.forEach(image => {
    imageObserver.observe(image);
  });

  // // Intersection Observer for Sections
  const sectionObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const section = entry.target;
        section.classList.add('visible');
        observer.unobserve(section);
      }
    });
  }, { threshold: 0.2 });

  lazySections.forEach(section => {
    sectionObserver.observe(section);
  });

  // Basic form validation
  document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    if (!name || !email || !message) {
      Swal.fire({
        title: 'Failed!',
        text: 'Please fill in all fields.',
        icon: 'error',
        confirmButtonText: 'Close'
      });
      return;
    }

    Swal.fire({
      title: 'Success!',
      text: 'Your message has been sent successfully!',
      icon: 'success',
      confirmButtonText: 'OK',
      timer: 2000,
      timerProgressBar: true
    });
    // Normally, you'd send this data to the server via AJAX
  });

  // Get the slider container and slides
  const slider = document.querySelector('.hero-slider');
  const slides = document.querySelectorAll('.slide');
  let currentSlide = 0;

  // Function to move to the next slide
  function nextSlide() {
    slides[currentSlide].classList.remove('active');
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].classList.add('active');
    updateSliderPosition();
  }

  // Function to update the slider position based on the current slide
  function updateSliderPosition() {
    slider.style.transform = `translateX(-${currentSlide * 100}%)`;
  }

  // Auto slide every 3 seconds
  setInterval(nextSlide, 10000);  // 3000ms = 3 seconds
});
  
$(document).ready(function(){
  $('.service-cards').slick({
    infinite: true,        
    slidesToShow: 3,      
    slidesToScroll: 1,     
    // autoplay: true,        
    // autoplaySpeed: 2000,  
    arrows: true,
    dots: true,
    responsive: [
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,  // Show 1 slide
          slidesToScroll: 1 // Scroll 1 slide
        }
      },
    ]
  });
});

// $(document).ready(function(){
//   $('.hero-slider').slick({
//     infinite: true,        
//     slidesToShow: 1,      
//     slidesToScroll: 1,     
//     autoplay: true,        
//     autoplaySpeed: 2000,  
//     arrows: true,
//     dots: true,
//     responsive: [
//       {
//         breakpoint: 768,
//         settings: {
//           slidesToShow: 1,
//           slidesToScroll: 1
//         }
//       },
//     ]
//   });
// });

