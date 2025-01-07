document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".form");
    const quantityInput = document.querySelector(".qty_input");

    // Prevent submission if quantity is empty or less than 1
    form.addEventListener("submit", function (event) {
        if (!quantityInput.value.trim() || parseInt(quantityInput.value) < 1) {
            event.preventDefault(); // Stop form submission
            alert("Quantity cannot be empty or less than 1.");
            quantityInput.focus();
        }
    });
});
