document.addEventListener("DOMContentLoaded", function () {
    const modalElement = document.getElementById('staticBackdrop');
    const modalProductName = document.getElementById('modal-product-name');
    const deleteButton = document.getElementById('delete-button');

    modalElement.addEventListener('show.bs.modal', function (event) {
        // Get the button that triggered the modal
        const button = event.relatedTarget;

        // Extract the product details from the button
        const productId = button.getAttribute('data-id');
        const productSize = button.getAttribute('data-size');
        const productName = button.getAttribute('data-name');
        const deleteUrl = button.getAttribute('data-url');

        // Update the modal text with the correct product name
        modalProductName.textContent = productName;

        // Update the delete button with the correct URL
        deleteButton.setAttribute('href', deleteUrl);
    });
});
