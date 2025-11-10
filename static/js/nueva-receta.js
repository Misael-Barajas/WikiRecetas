document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const dropZonePrompt = document.getElementById('dropZonePrompt');
    const previewContainer = document.getElementById('imagePreviewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const removeBtn = document.getElementById('removeImageBtn');
    const browseLink = document.querySelector('.browse-link');


browseLink.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    fileInput.click();
    });
    
    dropZone.addEventListener('click', () => {
        if (!dropZone.classList.contains('has-image')) {
            fileInput.click();
        }
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        if (!dropZone.classList.contains('has-image')) {
            dropZone.classList.add('dragover');
        }
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                dropZonePrompt.style.display = 'none';
                previewContainer.style.display = 'block';
                dropZone.classList.add('has-image');
            };
            reader.readAsDataURL(file);

        } else {
            alert("Por favor, selecciona solo archivos de imagen.");
        }
    }

    removeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        resetUploader();
    });
    function resetUploader() {
        imagePreview.src = '';
        fileInput.value = null;
        previewContainer.style.display = 'none';
        dropZonePrompt.style.display = 'block';
        dropZone.classList.remove('has-image');
    }
});