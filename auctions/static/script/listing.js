




document.addEventListener('DOMContentLoaded', ()=>{
    const toastTag = document.getElementById('watchlist-toast');
    const toastListing = new bootstrap.Toast(toastTag);
    const toastBody = document.querySelector('.toast-body');

    const csrfToken = document.querySelector("meta[name='csrf-token']").content 

    const watchlistBtn = document.getElementById('watchlistBtn');
    
    const watchlistCounter = document.getElementById('watchlist-counter');
    
    // Add to 'watchlist' script
    watchlistBtn.addEventListener('click', function () {
        
        // Requst backend to add listing to watchlist
        fetch('/toggle_watchlist', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            credentials: 'include'
        })
        // Fetch back response data
        .then(response => response.json())
        .then(data => {

            // Watchlist button click logic
            if (data.status === "added") {
                // Change watchlist button text and color
                watchlistBtn.classList.add('btn-danger')
                watchlistBtn.classList.remove('btn-dark')
                watchlistBtn.textContent = 'Remove'

                // Update watachlist counter indicator
                watchlistCounter.textContent = (Number(watchlistCounter.textContent) + 1).toString();
                if (watchlistCounter.classList.contains('no-show')) watchlistCounter.classList.remove('no-show');

            } else {
                // Change watchlist button text and color
                watchlistBtn.classList.add('btn-dark')
                watchlistBtn.classList.remove('btn-danger')
                watchlistBtn.textContent = 'Watchlist'

                // Update watachlist counter indicator
                let wathclistCount = Number(watchlistCounter.textContent) - 1;
                if (wathclistCount == 0) watchlistCounter.classList.add('no-show');
                
                watchlistCounter.textContent = wathclistCount.toString()
                
            }

            // Show toast
            toastBody.textContent = data.message;
            toastListing.show();
        })
    });


    // const bidInput = document.getElementById('bidInput');
    // const placeBid = document.getElementById('placeBid');
    
    // placeBid.addEventListener('click', function(){

    //     fetch(`/place_bid/${listingId}`, {
    //         method: 'POST',
    //         headers: {
    //             'X-CSRFToken': csrfToken,
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({'bid': bidInput.value})
    //     }) 

    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data.message);
    //         toastBody.textContent = data.message;
    //         toastListing.show();
    //     }) 
           
    // })
    

    
    

});