(function() {
    let page = 1;
    let loading = false;
    const container = document.getElementById('posts-container');
    let hasMore = container.dataset.hasMore === 'true';
    const loader = document.getElementById('loader');
    const endMessage = document.getElementById('end-message');
    
    function createPostHTML(post) {
        return `
            <article class="position-relative col-md-5 small" role="listitem">
                <div class="text-muted flex-shrink-0 article-date">
                    ${post.created_at.slice(0, 10)}
                </div>
                <div class="d-flex flex-column">
                    <div class="w-100 rounded-3 overflow-hidden mb-3">
                        <img src="${post.image}" class="img-fluid object-fit-cover">
                    </div>
                    <a href="/${post.author_username}" class="text-decoration-none text-dark fw-bold">@${post.author_username}</a>
                    <div>${post.content}</div>
                </div>
            </article>
        `;
    }
    
    async function loadMorePosts() {
        if (loading || !hasMore) return;
        
        loading = true;
        page++;
        
        try {
            const response = await fetch(`/api/posts?page=${page}`);
            const data = await response.json();
            
            data.posts.forEach(post => {
                container.insertAdjacentHTML('beforeend', createPostHTML(post));
            });
            
            console.log('loaded');
            hasMore = data.has_more;
            
            if (!hasMore) {
                loader.classList.add('d-none');
                endMessage.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Błąd ładowania postów:', error);
        } finally {
            loading = false;
        }
    }
    
    // Intersection Observer do wykrywania kiedy loader jest widoczny
    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && hasMore) {
            loadMorePosts();
        }
    }, {
        rootMargin: '100px' // Załaduj wcześniej, 100px przed końcem
    });
    
    observer.observe(loader);
})();