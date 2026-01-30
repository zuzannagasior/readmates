(function() {
    let page = 1;
    let loading = false;
    const container = document.getElementById('posts-container');
    let hasMore = container.dataset.hasMore === 'true';
    const loader = document.getElementById('loader');
    const endMessage = document.getElementById('end-message');
    
    async function loadMorePosts() {
        if (loading || !hasMore) return;
        
        loading = true;
        page++;
        
        try {
            const response = await fetch(`/api/posts?page=${page}`);
            const data = await response.json();
            
            container.insertAdjacentHTML('beforeend', data.html);
            
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
    
    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && hasMore) {
            loadMorePosts();
        }
    }, {
        rootMargin: '100px'
    });
    
    observer.observe(loader);
})();