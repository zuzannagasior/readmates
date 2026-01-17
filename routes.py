from flask import render_template


def register_routes(app):
    @app.route('/')
    def index():
        # TODO: Pobierz dane z bazy danych
        return render_template('index.html')

    @app.route('/post/<int:id>')
    def show_post(id):
        # TODO: Pobierz dane z bazy danych
        return render_template('post.html', id=id)

    @app.route('/<string:username>')
    def user(username):
        # TODO: Pobierz dane z bazy danych
        return render_template('user.html', username=username)

    @app.route('/create')
    def create():
        return render_template('create_post.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')
        