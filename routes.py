import json
from pathlib import Path
from flask import flash, jsonify, redirect, render_template, request, session, url_for
from database import db
from forms import LoginForm, RegistrationForm
from models import User
from functools import wraps

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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


def register_routes(app):
    @app.route('/')
    @login_required
    def home():
        posts = load_posts()
        initial_posts = posts[:POSTS_PER_PAGE]
        has_more = len(posts) > POSTS_PER_PAGE
        return render_template('home.html', posts=initial_posts, has_more=has_more)

    @app.route('/api/posts')
    @api_login_required
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
    @api_login_required
    def api_comments(post_id):
        """Endpoint API do pobierania komentarzy posta."""
        comments = load_comments()
        post_comments = comments.get(str(post_id), [])
        return jsonify({
            'comments': post_comments,
            'count': len(post_comments)
        })

    @app.route('/post/<int:id>')
    @login_required
    def show_post(id):
        # TODO: Pobierz dane z bazy danych
        return render_template('post.html', id=id)

    @app.route('/<string:username>')
    @login_required
    def user(username):
        posts = load_posts()
        latest_post = posts[0]
        other_posts = posts[1:]
        return render_template('user.html', username=username, latest_post=latest_post, other_posts=other_posts, posts_count=len(posts), comments_count=100)

    @app.route('/create', methods=['POST'])
    @login_required
    def create():
        image = request.form.get('image')
        content = request.form.get('content')
        # TODO: Zapisz post do bazy danych
        flash('Post został opublikowany!', 'success')
        return redirect(url_for('user', username='admin'))


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if 'user_id' in session:
            return redirect(url_for('home'))

        form = LoginForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()

            if not user or not user.check_password(password):
                flash('Nieprawidłowy login lub hasło', 'error')
                return redirect(url_for('login'))

            session['user_id'] = user.id
            session['username'] = user.username

            return redirect(url_for('home'))
        
        elif request.method == 'POST':
            flash('Popraw błędy w formularzu', 'error')

        return render_template('login.html', form=form)


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if 'user_id' in session:
            return redirect(url_for('home'))

        form = RegistrationForm()

        if form.validate_on_submit():      
            email = form.email.data 
            username = form.username.data
            password = form.password.data
            
            if User.query.filter_by(username=username).first():
                flash('Użytkownik już istnieje', 'error')
                return redirect(url_for('register'))

            if User.query.filter_by(email=email).first():
                flash('Email już istnieje', 'error')
                return redirect(url_for('register'))

            new_user = User(username=username, email=email)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))
        elif request.method == 'POST':
            flash('Popraw błędy w formularzu', 'error')

        return render_template('register.html', form=form)
        
    @app.route('/logout')
    def logout():
        session.clear()

        return redirect(url_for('login'))