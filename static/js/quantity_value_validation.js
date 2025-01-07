function validateQuantity(input) {
    if (input.value === "" || parseInt(input.value) < 1) {
        input.value = 1; // Set to minimum allowed value
    }
}
