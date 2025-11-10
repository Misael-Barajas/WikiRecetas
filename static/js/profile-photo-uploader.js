document.addEventListener('DOMContentLoaded', () => {
  const dropZone = document.getElementById('profileDropZone');
  const fileInput = document.getElementById('profilePicInput');
  const imagePreview = document.getElementById('profileImagePreview');
  const editBtn = document.getElementById('editProfileBtn');


  editBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
  });

  dropZone.addEventListener('click', () => {
    fileInput.click();
  });

  
  ['dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
    });
  });

  dropZone.addEventListener('dragover', () => {
  });

  dropZone.addEventListener('dragleave', () => {
  });

  dropZone.addEventListener('drop', (e) => {
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
      };
      
      reader.readAsDataURL(file);
    } else {
      alert("Por favor, selecciona solo archivos de imagen.");
    }
  }
  
});