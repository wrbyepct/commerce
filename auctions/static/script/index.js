import { watchlistBtnListen } from "./watchlist_btn.js";

document.addEventListener('DOMContentLoaded', function(){
    const descriptions = document.querySelectorAll('.description');
    let maxLength = 70;
    descriptions.forEach(description => {
        if (description.innerText.length > maxLength) {
            description.innerText = description.innerText.substr(0, maxLength) + '...';
        }
    })
    watchlistBtnListen();
})
