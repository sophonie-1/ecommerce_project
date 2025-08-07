document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.search-form');
    
    if (!form) {
        console.error('Form element with class "search-form" not found');
        return;
    }

    // Check if there was a previous submission and clear fields
    if (sessionStorage.getItem('formSubmitted')) {
        const searchInput = document.querySelector('#id_search_query');
        const categoryInput = document.querySelector('#id_category');
        if (searchInput) searchInput.value = '';
        if (categoryInput) categoryInput.value = '';
        sessionStorage.removeItem('formSubmitted'); // Clear the flag
    }

    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent default form submission
        const searchQuery = document.querySelector('#id_search_query')?.value.trim();
        const category = document.querySelector('#id_category')?.value;

        if (!searchQuery && !category) {
            event.preventDefault();
            alert('Please enter a search query or select a category.');
            return;
        }

        if (form.checkValidity()) {
            // Set a flag in sessionStorage to indicate submission
            sessionStorage.setItem('formSubmitted', 'true');
        }
    });
});