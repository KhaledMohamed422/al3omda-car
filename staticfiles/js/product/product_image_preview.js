document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('input[type="file"]').forEach(function (input) {
        input.addEventListener('change', function () {
            const file = this.files[0];
            if (!file) return;

            // Get the ID of the input and convert to matching preview img ID
            const inputId = this.id; // e.g., "id_images-0-image"
            const previewId = 'preview_' + inputId;

            let previewImg = document.getElementById(previewId);
            if (!previewImg) return;

            const reader = new FileReader();
            reader.onload = function (e) {
                previewImg.src = e.target.result;
                previewImg.style.display = 'block';
            };
            reader.readAsDataURL(file);
        });
    });
});
// This script listens for changes on file input elements and updates the corresponding image preview.