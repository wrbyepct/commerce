
import { watchlistBtnListen } from "./watchlist_btn.js";

document.addEventListener('DOMContentLoaded', ()=>{
    
    // Watchers tooltip 
    const watcherTooltip = document.querySelector('span[data-bs-toggle="tooltip"]');
    const enabledWatcherTooltip = new bootstrap.Tooltip(watcherTooltip);

    watchlistBtnListen();
    
    // Toggle comment editable mode
    const commentContainers = document.querySelectorAll('.comment-section--body');

    commentContainers.forEach(commentContainer => {
        
        const contentArea = commentContainer.querySelector('textarea');
        const originalCommentContent = contentArea.value;

        const editActionContainer = commentContainer.querySelector('.comment-secion--edit-actions');

        const editBtn = commentContainer.querySelector('.edit-btn');
        const cancelEditBtn = commentContainer.querySelector('.cancel-edit');
        

        const dropdown = commentContainer.querySelector('.dropdown');

        // Edit logic
        if (editBtn) {
            editBtn.addEventListener('click', function(){

                // Make the textarea editable
                contentArea.removeAttribute("disabled");

                contentArea.selectionStart = contentArea.value.length;
                contentArea.focus();
                
                editActionContainer.classList.toggle('d-none');
                dropdown.classList.toggle('d-none');
            });
    
        }

        // Cancel comment logic 
        cancelEditBtn.addEventListener('click', function(){

            contentArea.value = originalCommentContent;
            contentArea.setAttribute("disabled", true);

            editActionContainer.classList.toggle('d-none');
            dropdown.classList.toggle('d-none');

        });

   })


  


});