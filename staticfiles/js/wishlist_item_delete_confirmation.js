document.addEventListener('DOMContentLoaded', function () {
    var deleteWishlistModal = document.getElementById('deleteWishlistModal');

    deleteWishlistModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // The button that triggered the modal
        var itemUrl = button.getAttribute('data-url'); // Get URL for the product to be removed
        var itemName = button.getAttribute('data-name'); // Get product name

        var deleteForm = document.getElementById('delete-wishlist-form');
        var deleteMessage = document.getElementById('delete-wishlist-message');
        var productNameElement = document.getElementById('wishlist-product-name');

        // Update the modal content
        deleteForm.action = itemUrl; // Set the form action to the product's remove URL
        productNameElement.textContent = itemName; // Update the product name in the modal
    });
});
