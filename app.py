import os
from flask import Flask, render_template, session
from flask_wtf.csrf import CSRFProtect
from database import db
from routes import register_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twoj-sekretny-klucz-123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///readmates.db'

app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # max 5 MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
csrf = CSRFProtect(app)

register_routes(app)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html',
        error_code=404,
        error_title='Strona nie została znaleziona',
        error_message='Przepraszamy, ale strona której szukasz nie istnieje lub została przeniesiona.'
    ), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html',
        error_code=500,
        error_title='Błąd serwera',
        error_message='Przepraszamy, wystąpił nieoczekiwany błąd. Spróbuj ponownie później.'
    ), 500

with app.app_context():
    db.create_all()

@app.context_processor
def inject_globals():
    from models import User
    from forms import CreatePostForm
    
    user_id = session.get('user_id')
    if user_id:
        current_user = User.query.get(user_id)
        create_form = CreatePostForm()
    else:
        current_user = None
        create_form = None

    
    return dict(current_user=current_user, create_form=create_form)

if __name__ == '__main__':
    app.run(debug=True)