(function () {
    const commentsSection = document.querySelector('.comments-section');
    if (!commentsSection) return;

    const postId = commentsSection.dataset.postId;
    const commentsList = document.getElementById('inline-comments-list');
    const commentForm = document.getElementById('inline-comment-form');
    const commentInput = document.getElementById('inline-comment-input');
    const commentsCount = document.getElementById('comments-count');

    function createCommentHTML(comment) {
        return `
            <div class="comment mb-3 pb-3 border-bottom">
                <div class="d-flex justify-content-between align-items-start mb-1">
                    <a href="/${comment.author_username}" class="fw-bold text-decoration-none text-dark">
                        @${comment.author_username}
                    </a>
                    <small class="text-muted">${comment.created_at.slice(0, 10)}</small>
                </div>
                <p class="mb-0">${comment.content}</p>
            </div>
        `;
    }

    function showLoading() {
        commentsList.innerHTML = `
            <div class="d-flex justify-content-center py-4">
                <div class="spinner-border spinner-border-sm text-secondary" role="status">
                    <span class="visually-hidden">Ładowanie...</span>
                </div>
            </div>
        `;
    }

    function showEmpty() {
        commentsList.innerHTML = `
            <div class="text-center text-muted py-4">
                <p class="mb-0">Brak komentarzy</p>
                <small>Bądź pierwszy!</small>
            </div>
        `;
    }

    async function loadComments() {
        showLoading();

        try {
            const response = await fetch(`/api/posts/${postId}/comments`);
            const data = await response.json();

            commentsCount.textContent = data.count;

            if (data.comments.length === 0) {
                showEmpty();
            } else {
                commentsList.innerHTML = data.comments.map(createCommentHTML).join('');
            }
        } catch (error) {
            console.error('Błąd ładowania komentarzy:', error);
            commentsList.innerHTML = `
                <div class="text-center text-danger py-4">
                    Błąd ładowania komentarzy
                </div>
            `;
        }
    }

    commentForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const content = commentInput.value.trim();
        if (!content) return;

        const newComment = {
            id: Date.now(),
            author_username: 'ty',
            content: content,
            created_at: new Date().toISOString()
        };

        commentsList.insertAdjacentHTML('afterbegin', createCommentHTML(newComment));
        commentInput.value = '';

        // Aktualizuj licznik
        const currentCount = parseInt(commentsCount.textContent) || 0;
        commentsCount.textContent = currentCount + 1;
    });

    // Załaduj komentarze przy starcie strony
    loadComments();
})();
