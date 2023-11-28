
import { watchlistBtnListen } from "./watchlist_btn.js";

document.addEventListener('DOMContentLoaded', ()=>{
    
    // Watchers tooltip 
    const watcherTooltip = document.querySelector('span[data-bs-toggle="tooltip"]');
    const enabledWatcherTooltip = new bootstrap.Tooltip(watcherTooltip);

    watchlistBtnListen();
    
    const commentContainers = document.querySelectorAll('.comment-section--body');

    // Set Toggle comment editable mode logic
    commentContainers.forEach(commentContainer => {
        
        const contentArea = commentContainer.querySelector('textarea');
        const originalCommentContent = contentArea.value;

        // Container for save/cancel for editing
        const editActionContainer = commentContainer.querySelector('.comment-secion--edit-actions');

        // Dropdown actions
        const dropdown = commentContainer.querySelector('.dropdown');

        const editBtn = commentContainer.querySelector('.edit-btn');

        const saveEdit = commentContainer.querySelector('.save-edit');
        const cancelEditBtn = commentContainer.querySelector('.cancel-edit');
        
        
        // Edit logic - check if the comment belongs to the user
        if (editBtn) {
            editBtn.addEventListener('click', function(){

                // Make the textarea editable
                contentArea.removeAttribute("disabled");

                // Cursor to the end
                contentArea.selectionStart = contentArea.value.length;
                contentArea.focus();
                
                // Hide the comment action toggle
                editActionContainer.classList.toggle('d-none');
                dropdown.classList.toggle('d-none');
            });

            // Save edit button remains 'disabled' if the content doesn't change or is empty
            commentContainer.addEventListener('input', (event) => {
                if (event.target.value === "" || event.target.value === originalCommentContent) 
                    saveEdit.setAttribute('disabled', true);
                else
                    saveEdit.removeAttribute('disabled');
            })

            // Cancel comment logic 
            cancelEditBtn.addEventListener('click', function(){

                contentArea.value = originalCommentContent;
                contentArea.setAttribute("disabled", true);

                editActionContainer.classList.toggle('d-none');
                dropdown.classList.toggle('d-none');

            });
    
        }

   })

});