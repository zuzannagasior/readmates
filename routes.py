import os
import uuid
from flask import flash, jsonify, redirect, render_template, request, session, url_for, current_app
from database import db
from forms import CommentForm, CreatePostForm, LoginForm, RegistrationForm
from models import Comment, User, Post, SavedPost
from functools import wraps
from werkzeug.utils import secure_filename

POSTS_PER_PAGE = 8

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def register_routes(app):
    @app.route('/')
    @login_required
    def home():
        pagination = Post.query.order_by(Post.created_at.desc()).paginate(
            page=1, 
            per_page=POSTS_PER_PAGE, 
            error_out=False
        )
        saved_post_ids = set(
            sp.post_id for sp in SavedPost.query.filter_by(user_id=session['user_id']).all()
        )

        return render_template(
            'home.html', 
            posts=pagination.items, 
            has_more=pagination.has_next, 
            saved_post_ids=saved_post_ids
        )
    
    @app.route('/api/posts')
    @api_login_required
    def api_posts():
        page = request.args.get('page', 1, type=int)
        pagination = Post.query.order_by(Post.created_at.desc()).paginate(
            page=page,
            per_page=POSTS_PER_PAGE,
            error_out=False
        )
        
        saved_post_ids = set(
            sp.post_id for sp in SavedPost.query.filter_by(user_id=session['user_id']).all()
        )
        
        html = render_template(
            'partials/posts_list.html',
            posts=pagination.items,
            saved_post_ids=saved_post_ids
        )
        
        return jsonify({
            'html': html,
            'has_more': pagination.has_next,
            'page': page
        })
      
    @app.route('/post/<string:id>')
    @login_required
    def show_post(id):
        post = Post.query.get_or_404(id)
        comments = Comment.query.filter_by(post_id=id).order_by(Comment.created_at.desc()).all()
        comment_form = CommentForm()
        
        is_saved = SavedPost.query.filter_by(user_id=session['user_id'], post_id=id).first() is not None
        saves_count = SavedPost.query.filter_by(post_id=id).count()
        
        return render_template('post.html', post=post, comments=comments, comment_form=comment_form, is_saved=is_saved, saves_count=saves_count)

    @app.route('/post/<string:id>/comment', methods=['POST'])
    @login_required
    def add_comment(id):
        post = Post.query.get_or_404(id)
        form = CommentForm()
        
        if form.validate_on_submit():
            comment = Comment(
                content=form.content.data,
                post_id=id,
                user_id=session['user_id']
            )
            db.session.add(comment)
            db.session.commit()
        
        if request.headers.get('HX-Request'):
            comments = Comment.query.filter_by(post_id=id).order_by(Comment.created_at.desc()).all()
            comment_form = CommentForm()
            return render_template('partials/comments.html', post=post, comments=comments, comment_form=comment_form, is_htmx=True)
        
        if form.validate_on_submit():
            flash('Komentarz został dodany', 'success')
        else:
            flash('Error. Spróbuj ponownie później', 'error')
        return redirect(url_for('show_post', id=id))

    @app.route('/post/<string:id>/delete', methods=['POST'])    
    @login_required
    def delete_post(id):
        post = Post.query.get_or_404(id)
        
        if post.user_id != session['user_id']:
            flash('Nie masz uprawnień do usunięcia tego posta', 'error')
            return redirect(url_for('show_post', id=id))
        
        if post.image_url:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(post.image_url))
            if os.path.exists(image_path):
                os.remove(image_path)
        
        db.session.delete(post)
        db.session.commit()
        
        flash('Post został usunięty', 'success')
        return redirect(url_for('user', username=session['username']))

    @app.route('/<string:username>')
    @login_required
    def user(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            # TODO: Wyświetl stronę 404
            return redirect(url_for('home'))
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
        latest_post = posts[0] if posts else None
        other_posts = posts[1:] if posts else []
        comments_count = user.comments_count()
        saved_posts = user.get_saved_posts()
        saved_count = len(saved_posts)

        return render_template('user.html', username=user.username, latest_post=latest_post, other_posts=other_posts, posts_count=len(posts), comments_count=user.comments_count(), saved_posts=saved_posts, saved_count=saved_count)

    @app.route('/create', methods=['POST'])
    @login_required
    def create():
        form = CreatePostForm()

        if form.validate_on_submit():
            file = form.image.data
           
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{uuid.uuid4().hex}.{ext}"

                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                image_url = f"uploads/{filename}"
            else:
                flash('Nieprawidłowy format pliku', 'error')
                return redirect(url_for('home'))

            post = Post(
                title=form.title.data,
                content=form.content.data,
                image_url=image_url,
                user_id=session['user_id']
            )

            db.session.add(post)
            db.session.commit()

        else:
            flash('Popraw błędy w formularzu', 'error')
            return redirect(url_for('home'))
            
        flash('Post został zapisany!', 'success')
        return redirect(url_for('user', username=session['username']))

    @app.route('/post/<string:id>/save', methods=['POST'])
    @api_login_required
    def toggle_save_post(id):
        try:
            post = Post.query.get_or_404(id)
            user_id = session['user_id']
            
            if post.user_id == user_id:
                return jsonify({'error': 'Nie możesz zapisać własnego posta'}), 403

            existing_save = SavedPost.query.filter_by(user_id=user_id, post_id=id).first()
            
            if existing_save:
                db.session.delete(existing_save)
                db.session.commit()
                is_saved = False
            else:
                saved_post = SavedPost(user_id=user_id, post_id=id)
                db.session.add(saved_post)
                db.session.commit()
                is_saved = True
            
            saves_count = SavedPost.query.filter_by(post_id=id).count()
            
            return jsonify({
                'is_saved': is_saved,
                'saves_count': saves_count
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


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
