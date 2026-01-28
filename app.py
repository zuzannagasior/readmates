import os
from flask import Flask, session
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

with app.app_context():
    db.create_all()

@app.context_processor
def inject_globals():
    from models import User
    from forms import CreatePostForm
    
    user_id = session.get('user_id')
    if user_id:
        current_user = User.query.get(user_id)
        create_post_form = CreatePostForm()
    else:
        current_user = None
        create_post_form = None
    
    return dict(current_user=current_user, form=create_post_form)

if __name__ == '__main__':
    app.run(debug=True)