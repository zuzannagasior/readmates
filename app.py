from flask import Flask
from flask_wtf.csrf import CSRFProtect
from database import db
from routes import register_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twoj-sekretny-klucz-123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///readmates.db'

db.init_app(app)
csrf = CSRFProtect(app)

register_routes(app)

with app.app_context():
    db.create_all()

@app.context_processor
def inject_user():
    current_user = {
        'username': 'admin',
    }
    return dict(current_user=current_user)

if __name__ == '__main__':
    app.run(debug=True)