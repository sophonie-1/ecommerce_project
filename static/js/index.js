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
        const sortByInput = document.querySelector('#id_sort_by');
        if (sortByInput) sortByInput.value = ''; // Clear sort by field
        if (searchInput) searchInput.value = '';
        if (categoryInput) categoryInput.value = '';
        sessionStorage.removeItem('formSubmitted'); // Clear the flag
    }

    form.addEventListener('submit', (event) => {
        
        const searchQuery = document.querySelector('#id_search_query')?.value.trim();
        const category = document.querySelector('#id_category')?.value;
        const sortBy = document.querySelector('#id_sort_by')?.value;
        console.log('Search Query:', sortBy);

        if (!searchQuery && !category && !sortBy) {
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
