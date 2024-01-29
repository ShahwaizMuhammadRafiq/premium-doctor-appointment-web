// static/script.js
document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        document.getElementById('content').style.display = 'block';
        document.querySelector('.loader-container').style.display = 'none';
    }, 3000); // Adjust the delay time as needed (3000 milliseconds = 3 seconds)
});
document.addEventListener("DOMContentLoaded", function () {
    // Add event listener to the form
    var contactForm = document.getElementById("contact");
    if (contactForm) {
        contactForm.addEventListener("submit", function (event) {
            // Prevent the form from submitting
            event.preventDefault();

            // Perform form validation
            if (validateForm()) {
                // If the form is valid, you can handle the form submission here
                alert("Form submitted successfully!");
                // You may want to send the form data to a server using AJAX or other methods
            }
        });
    }

    // Function to validate the form
    function validateForm() {
        var nameInput = document.getElementById("name");
        var emailInput = document.getElementById("email");
        var subjectInput = document.getElementById("subject");
        var messageInput = document.getElementById("message");

        // Simple validation for demonstration purposes
        if (nameInput.value.trim() === "" || emailInput.value.trim() === "" || subjectInput.value.trim() === "" || messageInput.value.trim() === "") {
            alert("Please fill in all fields.");
            return false;
        }

        // You can add more sophisticated validation logic as needed

        return true; // Form is valid
    }
});
let slideIndex = 0;

function showSlide(index) {
    const slides = document.querySelector('.slider');
    const totalSlides = document.querySelectorAll('.slide').length;

    if (index >= totalSlides) {
        slideIndex = 0;
    } else if (index < 0) {
        slideIndex = totalSlides - 1;
    } else {
        slideIndex = index;
    }

    const translateValue = -slideIndex * 100 + '%';
    slides.style.transform = `translateX(${translateValue})`;
}

function nextSlide() {
    showSlide(slideIndex + 1);
}

function prevSlide() {
    showSlide(slideIndex - 1);
}

// Auto slide (optional)
setInterval(nextSlide, 3000); // Change slide every 3 seconds

