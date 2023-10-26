




document.addEventListener('DOMContentLoaded', ()=>{
    const toastTag = document.getElementById('watchlist-toast');
    const toastListing = new bootstrap.Toast(toastTag);
    const toastBody = document.querySelector('.toast-body');

    const csrfToken = document.querySelector("meta[name='csrf-token']").content 

    const watchlistBtn = document.getElementById('watchlistBtn');
    const listingId = watchlistBtn.getAttribute("data-custom");


    watchlistBtn.addEventListener('click', function () {
        
        // Fetch data from backend
        fetch(`/toggle_watchlist/${listingId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {

            // This is for immediate change effect
            if (data.status === "added") {
                watchlistBtn.classList.add('btn-danger')
                watchlistBtn.classList.remove('btn-dark')
                watchlistBtn.textContent = 'Remove'
            } else {
                watchlistBtn.classList.add('btn-dark')
                watchlistBtn.classList.remove('btn-danger')
                watchlistBtn.textContent = 'Watchlist'
            }
            toastBody.textContent = data.message;
            toastListing.show();
        })
    });

});