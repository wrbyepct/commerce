


export function watchlistBtnListen() {
    const toastTag = document.getElementById('watchlist-toast');
    const toastListing = new bootstrap.Toast(toastTag);
    const toastBody = document.querySelector('.toast-body');

    const csrfToken = document.querySelector("meta[name='csrf-token']").content 

    const watchlistBtns = document.querySelectorAll('.watchlist-btn');
    const watchlistCounter = document.getElementById('watchlist-counter');
    
    watchlistBtns.forEach(watchlistBtn => {
        // Add to 'watchlist' script
        if (watchlistBtn) {
            const listingID = watchlistBtn.getAttribute('item-id');
            watchlistBtn.addEventListener('click', function () {
                
                // Requst backend to add listing to watchlist
                fetch(`/toggle_watchlist/${listingID}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    credentials: 'include'
                })
                // Fetch back response data
                .then(response => response.json())
                .then(data => {

                    const icon = document.createElement('i');
                    const buttonText = document.createElement('span');

                    // Watchlist button click logic
                    if (data.status === "added") {
                        // Change watchlist button text and color
                        watchlistBtn.classList.add('btn-danger');
                        watchlistBtn.classList.remove('btn-outline-dark');

                        watchlistBtn.textContent = "";
                        buttonText.textContent = ' On watchlist';
                        icon.className = 'bi bi-heart-fill';
                        
                        // Update watachlist counter indicator
                        watchlistCounter.textContent = (Number(watchlistCounter.textContent) + 1).toString();
                        if (watchlistCounter.classList.contains('d-none')) watchlistCounter.classList.remove('d-none');
        
                    } else {
                        // Change watchlist button text and color
                        watchlistBtn.classList.add('btn-outline-dark');
                        watchlistBtn.classList.remove('btn-danger');

                        watchlistBtn.textContent = "";
                        buttonText.textContent = ' Watchlist';
                        icon.className = 'bi bi-heart';
        
                        // Update watachlist counter indicator
                        let wathclistCount = Number(watchlistCounter.textContent) - 1;
                        if (wathclistCount == 0) watchlistCounter.classList.add('d-none');
                        
                        watchlistCounter.textContent = wathclistCount.toString()
                        
                    }
                    
                    watchlistBtn.append(icon, buttonText);

                    // Show toast
                    toastBody.textContent = data.message;
                    toastListing.show();
                })
                .catch(error => console.error(error))
            });
        }
    })

}


 