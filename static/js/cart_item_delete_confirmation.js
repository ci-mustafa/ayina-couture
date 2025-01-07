document.addEventListener("DOMContentLoaded", function () {
    // Attach the modal shown event listener
    const deleteButton = document.getElementById('delete-button');
    const modalElement = document.getElementById('staticBackdrop');

    modalElement.addEventListener('show.bs.modal', function () {
        // Get the delete URL when the modal is shown
        const deleteUrl = deleteButton.getAttribute('data-url');

        // Set the href of the delete button in the modal
        const confirmDeleteButton = document.getElementById('delete-button');
        confirmDeleteButton.setAttribute('href', deleteUrl);
    });
});