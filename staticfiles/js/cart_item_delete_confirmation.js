// document.addEventListener("DOMContentLoaded", function () {
//     const modalElement = document.getElementById('staticBackdrop');
//     const modalProductName = document.getElementById('modal-product-name');
//     const deleteButton = document.getElementById('delete-button');

//     modalElement.addEventListener('show.bs.modal', function (event) {
//         // Get the button that triggered the modal
//         const button = event.relatedTarget;

//         // Extract the product details from the button
//         const productId = button.getAttribute('data-id');
//         const productSize = button.getAttribute('data-size');
//         const productName = button.getAttribute('data-name');
//         const deleteUrl = button.getAttribute('data-url');

//         // Update the modal text with the correct product name
//         modalProductName.textContent = productName;

//         // Update the delete button with the correct URL
//         deleteButton.setAttribute('href', deleteUrl);
//     });
// });

// JavaScript to handle dynamic modal content based on deletion type
var deleteItemModal = document.getElementById('deleteItemModal'); 

deleteItemModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget; // The button that triggered the modal
    var itemUrl = button.getAttribute('data-url'); // Get URL for item to be deleted
    var isDeleteAll = button.getAttribute('data-all'); // Check if it's "Delete All Items" button
    
    var deleteForm = document.getElementById('delete-item-form');
    var deleteButton = document.getElementById('delete-button');
    var deleteMessage = document.getElementById('delete-item-message');
    
    if (isDeleteAll) {
        // If deleting all items
        deleteForm.action = itemUrl;  // Set action to delete all items URL
        deleteMessage.innerHTML = 'Are you sure you want to delete all items from the cart? This action cannot be undone.';
        deleteButton.innerHTML = 'Delete All Items';
    } else {
        // If deleting a single item
        deleteForm.action = itemUrl;  // Set action to delete specific item URL
        deleteMessage.innerHTML = 'Are you sure you want to delete this item from the cart? This action cannot be undone.';
        deleteButton.innerHTML = 'Delete Item';
    }
});


