document.addEventListener('DOMContentLoaded', function () {
    const dropdownContainer = document.querySelector('.dropdown-content');
    const selectedMonthDisplay = document.getElementById('selected-month');
    const prevMonthSalesDisplay = document.getElementById('prev-month-sales');
    const fullUrl = window.location.href;
    const urlParts = fullUrl.split("?");
    const lastPart = urlParts[0];

    // Close product detail when close button is clicked
    document.getElementById('close-detail').addEventListener('click', function() {
        // Change main table to original display    
        document.getElementById('main-content-opened').setAttribute("id", "main-content");
            
        // Return to last url
        window.location.href = lastPart;
    });

    if (dropdownContainer) {
        dropdownContainer.addEventListener('click', function (event) {
            if (event.target.classList.contains('month-option')) {
                console.log('Button Clicked'); // Debug
                const selectedMonth = event.target.getAttribute('data-month');
                const productName = event.target.getAttribute('data-product');

                console.log('Selected month:', selectedMonth, 'Product:', productName); // Debug

                // Update displayed month
                if (selectedMonthDisplay) {
                    selectedMonthDisplay.textContent = selectedMonth;
                } else {
                    console.error('selected-month element not found');
                }

                // Fetch sales data
                fetch(`/report/best-product?chosen=${encodeURIComponent(productName)}&prev-month=${encodeURIComponent(selectedMonth)}`, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-Custom-Partial-Request': 'true'
                    },
                })
                .then(response => {
                    console.log('Response status:', response.status); // Debug
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Received data:', data); // Debug
                    if (prevMonthSalesDisplay) {
                        prevMonthSalesDisplay.textContent = data.chosen_month_sale || '0';
                    } else {
                        console.error('prev-month-sales element not found');
                    }
                })
                .catch(error => {
                    console.error('Error fetching sales data:', error);
                    if (prevMonthSalesDisplay) {
                        prevMonthSalesDisplay.textContent = 'Error';
                    }
                });
            }
        });
    } else {
        console.error('Dropdown container not found');
    }
});
