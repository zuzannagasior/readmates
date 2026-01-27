import json
from pathlib import Path
from flask import flash, jsonify, redirect, render_template, request, url_for
from forms import LoginForm, RegistrationForm

POSTS_PER_PAGE = 3


def load_posts():
    """Wczytuje testowe dane postów z pliku JSON."""
    posts_path = Path(__file__).parent / 'data' / 'posts.json'
    with open(posts_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_comments():
    """Wczytuje testowe dane komentarzy z pliku JSON."""
    comments_path = Path(__file__).parent / 'data' / 'comments.json'
    with open(comments_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def register_routes(app):
    @app.route('/')
    def home():
        posts = load_posts()
        initial_posts = posts[:POSTS_PER_PAGE]
        has_more = len(posts) > POSTS_PER_PAGE
        return render_template('home.html', posts=initial_posts, has_more=has_more)

    @app.route('/api/posts')
    def api_posts():
        page = request.args.get('page', 1, type=int)
        posts = load_posts()
        
        start = (page - 1) * POSTS_PER_PAGE
        end = start + POSTS_PER_PAGE
        paginated_posts = posts[start:end]
        
        has_more = end < len(posts)
        
        return jsonify({
            'posts': paginated_posts,
            'has_more': has_more,
            'page': page
        })

    @app.route('/api/posts/<int:post_id>/comments')
    def api_comments(post_id):
        """Endpoint API do pobierania komentarzy posta."""
        comments = load_comments()
        post_comments = comments.get(str(post_id), [])
        return jsonify({
            'comments': post_comments,
            'count': len(post_comments)
        })

    @app.route('/post/<int:id>')
    def show_post(id):
        # TODO: Pobierz dane z bazy danych
        return render_template('post.html', id=id)

    @app.route('/<string:username>')
    def user(username):
        posts = load_posts()
        latest_post = posts[0]
        other_posts = posts[1:]
        return render_template('user.html', username=username, latest_post=latest_post, other_posts=other_posts, posts_count=len(posts), comments_count=100)

    @app.route('/create', methods=['POST'])
    def create():
        image = request.form.get('image')
        content = request.form.get('content')
        # TODO: Zapisz post do bazy danych
        flash('Post został opublikowany!', 'success')
        return redirect(url_for('user', username='admin'))


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            if username == 'admin' and password == 'secret':
                return redirect(url_for('home'))
            else:
                flash('Nieprawidłowy login lub hasło', 'danger')

        return render_template('login.html', form=form)


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()

        if form.validate_on_submit():
            email = form.email.data 
            # TODO: Sprawdź czy username jest już zarejestrowany
            username = form.username.data
            password = form.password.data
            # TODO: Zapisz użytkownika do bazy danych
            return redirect(url_for('home'))
       
                   
        return render_template('register.html', form=form)
        
    @app.route('/logout')
    def logout():
        return redirect(url_for('login'))