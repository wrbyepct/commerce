


export function watchlistBtnListen() {
    const toastTag = document.getElementById('watchlist-toast');
    const toastListing = new bootstrap.Toast(toastTag);
    const toastBody = document.querySelector('.toast-body');

    const csrfToken = document.querySelector("meta[name='csrf-token']").content 

    const watchlistBtns = document.querySelectorAll('.watchlist-btn');
    const watchlistCounter = document.getElementById('watchlist-counter');
    
    const watchersCount = document.getElementById('watchersCount');
    const watcherTooltip = document.getElementById('watcherTooltip');

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

                        // Change watchlist text and content
                        watchlistBtn.textContent = "";  
                        buttonText.textContent = ' WATCHING';
                        icon.className = 'bi bi-heart-fill';
                        
                        // Update watachlist counter indicator
                        watchlistCounter.textContent = (Number(watchlistCounter.textContent) + 1).toString();
                        if (watchlistCounter.classList.contains('d-none')) watchlistCounter.classList.remove('d-none');

                        // Update watchers count 
                        if (watchersCount) {
                            const count = Number(watchersCount.textContent) + 1;
                            watchersCount.textContent = count ;

                            watcherTooltip.setAttribute('title', `${count} watchers`)
                            new bootstrap.Tooltip(watcherTooltip);
                        }
        
                    } else {
                        // Change watchlist button text and color
                        watchlistBtn.classList.add('btn-outline-dark');
                        watchlistBtn.classList.remove('btn-danger');

                        watchlistBtn.textContent = "";
                        buttonText.textContent = ' WATCH';
                        icon.className = 'bi bi-heart';
        
                        // Update watachlist counter indicator
                        let wathclistCount = Number(watchlistCounter.textContent) - 1;
                        if (wathclistCount == 0) watchlistCounter.classList.add('d-none');
                        
                        watchlistCounter.textContent = wathclistCount.toString()
                        
                        // Update watchers count 
                        if (watchersCount) {
                            const count = Number(watchersCount.textContent) - 1;
                            watchersCount.textContent = count ;
                           
                            watcherTooltip.setAttribute('title', `${count} watchers`)
                            new bootstrap.Tooltip(watcherTooltip);
                        }
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


 