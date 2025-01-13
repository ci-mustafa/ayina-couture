// Check if there are any messages and display the toast
$(document).ready(function() {
    // Display all toasts
    var toasts = document.querySelectorAll('.toast');
    toasts.forEach(function(toast) {
        new bootstrap.Toast(toast).show(); // Show the toast using Bootstrap
    });
});