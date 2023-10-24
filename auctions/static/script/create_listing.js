
const showPreview = (file) => {
    const imagePreview = document.getElementById('imagePreview');

    if (file) {
        const reader = new FileReader();
        imagePreview.style.display = "block";

        // Set event listener on 'loaded', this means when it's done reading the file
        // then set the src as the resulted url
        reader.addEventListener('load', function() {
            imagePreview.setAttribute('src', this.result);
        });

        // Start reading image data as url 
        reader.readAsDataURL(file);
    }
}

const changeBorderColor = (element, style) => {
    element.style.border = style;
}

function addListEventAction(element, eventNames, changeBorderColor, style) {
    eventNames.forEach(eventName => {
        element.addEventListener(eventName, function(e){
            e.preventDefault();
            e.stopPropagation();
            changeBorderColor(element, style);
        })
    } )
}


function uploadImageEventHandler(e) {
    const dragArea = document.getElementById('dragArea');
    const imageInput = document.getElementById('id_image');

    if (e.type == "drop") {
        // If event if drop, we just need this extra step to assign file to image input field
        // The event target would be 'dropArea'
        imageInput.files = e.dataTransfer.files;
    } 

    const file = imageInput.files[0];
    showPreview(file);
    dragArea.style.display = 'none';

}


document.addEventListener('DOMContentLoaded', ()=> {
    const dropArea = document.getElementById('dropArea');

    // Seeting up drag and drop effect for image upload box 
    addListEventAction(
        dropArea, 
        ['dragenter', 'dragover'], 
        changeBorderColor, 
        "2px dashed blue"
    );
    
    addListEventAction(
        dropArea, 
        ['dragleave', 'drop'],
         changeBorderColor, 
         "1px solid black"
    );

    // Handle upload image by dropping or imageInputChanging
    // The 'dropArea' will know change in image input
    ['change', 'drop'].forEach(eventName =>{
        dropArea.addEventListener(eventName, uploadImageEventHandler)
    })


});