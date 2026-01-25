(function() {
    const commentsPanel = document.getElementById('commentsPanel');
    const commentsList = document.getElementById('comments-list');
    const commentForm = document.getElementById('comment-form');
    const commentInput = document.getElementById('comment-input');
    
    let currentPostId = null;
    
    function createCommentHTML(comment) {
        return `
            <div class="comment mb-3 pb-3 border-bottom">
                <div class="d-flex justify-content-between align-items-start mb-1">
                    <a href="/${comment.author_username}" class="fw-bold text-decoration-none text-dark">
                        @${comment.author_username}
                    </a>
                    <small class="text-muted">${comment.created_at.slice(0, 10)}</small>
                </div>
                <p class="mb-0 small">${comment.content}</p>
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
    
    async function loadComments(postId) {
        showLoading();
        
        try {
            const response = await fetch(`/api/posts/${postId}/comments`);
            const data = await response.json();
            
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
    
    commentsPanel.addEventListener('show.bs.offcanvas', function(event) {
        const button = event.relatedTarget;
        if (button) {
            currentPostId = button.dataset.postId;
            loadComments(currentPostId);
        }
    });
    
    commentsPanel.addEventListener('hidden.bs.offcanvas', function() {
        commentsList.innerHTML = '';
        commentInput.value = '';
        currentPostId = null;
    });
    
    commentForm.addEventListener('submit', function(e) {
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
    });
})();

