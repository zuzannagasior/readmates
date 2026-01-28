(function() {
    const imagePreview = document.getElementById('image-preview');
    const imagePreviewImage = document.getElementById('image-preview-img');
    const fileUploadArea = document.getElementById('file-upload-area');
    const fileInput = document.getElementById('image');

    document.getElementById('image').addEventListener('change', function (e) {
        const file = e.target.files[0];

        if (file) {
          const reader = new FileReader();
          reader.onload = function (e) {
            imagePreviewImage.src = e.target.result;
            imagePreview.classList.remove('d-none');
            fileUploadArea.classList.add('d-none');
          };
          reader.readAsDataURL(file);
        }
      });

      document.getElementById('remove-image-btn').addEventListener('click', function() {
        imagePreviewImage.src = '';
        imagePreview.classList.add('d-none');
        fileUploadArea.classList.remove('d-none');
        fileInput.value = '';
    });

    document.getElementById('createPostModal').addEventListener('hidden.bs.modal', function() {
        this.querySelector('form').reset();
        
        imagePreviewImage.src = '';
        imagePreview.classList.add('d-none');
        fileUploadArea.classList.remove('d-none');
        
        this.querySelectorAll('.error').forEach(el => el.remove());
    });
})()