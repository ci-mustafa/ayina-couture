// Show the popup when the page loads
$(document).ready(function () {
    $('#freeDeliveryPopup').fadeIn(); // Show the popup with a fade-in effect
});

// Close the popup when the user clicks the close button
$('#popupCloseBtn').click(function () {
    $('#freeDeliveryPopup').fadeOut(); // Hide the popup with a fade-out effect
});