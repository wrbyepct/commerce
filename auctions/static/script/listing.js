




document.addEventListener('DOMContentLoaded', ()=>{
    const toastTag = document.getElementById('watchlist-toast');
    const toastListing = new bootstrap.Toast(toastTag);
    const toastBody = document.querySelector('.toast-body');

    const csrfToken = document.querySelector("meta[name='csrf-token']").content 

    const watchlistBtn = document.getElementById('watchlistBtn');
    
    const watchlistCounter = document.getElementById('watchlist-counter');
    
    // Add to 'watchlist' script
    if (watchlistBtn) {
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
                    watchlistBtn.classList.add('btn-danger');
                    watchlistBtn.classList.remove('btn-dark');
                    watchlistBtn.textContent = 'Remove';
    
                    // Update watachlist counter indicator
                    watchlistCounter.textContent = (Number(watchlistCounter.textContent) + 1).toString();
                    if (watchlistCounter.classList.contains('d-none')) watchlistCounter.classList.remove('d-none');
    
                } else {
                    // Change watchlist button text and color
                    watchlistBtn.classList.add('btn-dark');
                    watchlistBtn.classList.remove('btn-danger');
                    watchlistBtn.textContent = 'Watchlist';
    
                    // Update watachlist counter indicator
                    let wathclistCount = Number(watchlistCounter.textContent) - 1;
                    if (wathclistCount == 0) watchlistCounter.classList.add('d-none');
                    
                    watchlistCounter.textContent = wathclistCount.toString()
                    
                }
    
                // Show toast
                toastBody.textContent = data.message;
                toastListing.show();
            })
            .catch(error => console.error(error))
        });
    }
    

   const commentContainers = document.querySelectorAll('.comment-section--body');

   commentContainers.forEach(commentContainer => {
        const commentId = commentContainer.getAttribute('data-comment-id');

        const contentArea = commentContainer.querySelector('textarea');
        const originalCommentContent = contentArea.value;

        const editActionContainer = commentContainer.querySelector('.comment-secion--edit-actions');

        const editBtn = commentContainer.querySelector('.edit-btn');
        const cancelEditBtn = commentContainer.querySelector('.cancel-edit');
        const saveEditBtn = commentContainer.querySelector('.save-edit');

        const dropdown = commentContainer.querySelector('.dropdown');

        // Edit logic
        if (editBtn) {
            editBtn.addEventListener('click', function(){

                contentArea.removeAttribute("disabled");

                contentArea.selectionStart = contentArea.value.length;
                contentArea.focus();
                
                editActionContainer.classList.toggle('d-none');
                dropdown.classList.toggle('d-none');
            });
    
        }

        // Cancel logic 
        cancelEditBtn.addEventListener('click', function(){

            contentArea.value = originalCommentContent;
            contentArea.setAttribute("disabled", true);

            editActionContainer.classList.toggle('d-none');
            dropdown.classList.toggle('d-none');
        });

   })


});