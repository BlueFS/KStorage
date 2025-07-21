// Script from Bulma's Documentation
// Script for the navbar burger
// Pre-loads page
document.addEventListener('DOMContentLoaded', () => {

    // Get all elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Adds click events
    $navbarBurgers.forEach(el => {
        el.addEventListener('click', () => {

            // Get the target from the "data-target" attribute
            const target = el.dataset.target;
            const $target = document.getElementById(target);

            // Toggle is set active and vice versa
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');

        });
    });
    // ChatGPT was used to learn/get new code for uploading files and previewing images
    // Script to upload files and show images
    const fileInput = document.querySelector("#file-upload input[type=file]");
    const fileNameBox = document.getElementById("file-name-box");
    const previewImage = document.getElementById("preview-image");
    const fileLabel = document.getElementById("file-label");
    const fileIcon = document.getElementById("file-icon");

    // Custom icons for non-image types
    const ICONS = {
        zip: "https://img.icons8.com/fluency/48/000000/zip.png",
        pdf: "https://img.icons8.com/fluency/48/000000/pdf.png",
        default: "https://img.icons8.com/fluency/48/000000/file.png"
    };

    fileInput.onchange = () => {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            fileNameBox.textContent = file.name;

            const extension = file.name.split('.').pop().toLowerCase();

            // If image, preview actual image
            if (file.type.startsWith("image/")) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewImage.style.display = "block";
                    fileLabel.style.display = "none";
                    fileIcon.style.display = "none";
                };
                reader.readAsDataURL(file);
            } else {
                // Show icon based on file type
                if (extension === "zip") {
                    previewImage.src = ICONS.zip;
                } else if (extension === "pdf") {
                    previewImage.src = ICONS.pdf;
                } else {
                    previewImage.src = ICONS.default;
                }
                previewImage.style.display = "block";
                fileLabel.style.display = "none";
                fileIcon.style.display = "none";
            }
        }
    };
});
