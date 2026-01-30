document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.save-post-btn').forEach(btn => {
        btn.addEventListener('click', async (event) => {
            const button = event.currentTarget;
            const postId = button.dataset.postId;
            const csrfToken = button.dataset.csrf;
            const icon = button.querySelector('i');
            const countEl = button.querySelector('.saves-count, #saves-count');

            const formData = new FormData();
            formData.append('csrf_token', csrfToken);

            try {
                const response = await fetch('/post/' + postId + '/save', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    countEl.textContent = data.saves_count;

                    if (data.is_saved) {
                        button.classList.add('saved');
                        button.title = 'Usuń z biblioteki';
                        icon.classList.remove('bi-bookmark-heart');
                        icon.classList.add('bi-bookmark-heart-fill');
                    } else {
                        button.classList.remove('saved');
                        button.title = 'Zapisz w bibliotece';
                        icon.classList.remove('bi-bookmark-heart-fill');
                        icon.classList.add('bi-bookmark-heart');
                    }
                }
            } catch (error) {
                console.error('Błąd podczas zapisywania:', error);
            }
        });
    });
});
