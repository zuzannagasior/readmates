from flask import flash, redirect, render_template, url_for

from forms import LoginForm, RegistrationForm


def register_routes(app):
    @app.route('/')
    def home():
        # TODO: Pobierz dane z bazy danych
        return render_template('home.html')

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
        