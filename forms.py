from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username',
                          validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Hasło',
                            validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Zaloguj się')

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                       validators=[DataRequired(), Email()])
    username = StringField('Username',
                          validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Hasło',
                            validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Potwierdź hasło',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')


class CreatePostForm(FlaskForm):
    title = StringField('Tytuł',
                        validators=[DataRequired(), Length(min=3, max=200)])
    content = TextAreaField('Treść',
                            validators=[DataRequired()])
    image = FileField('Zdjęcie',
                      validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg', 'gif', 'webp'], 'Only images are allowed')])
    submit = SubmitField('Opublikuj')

class CommentForm(FlaskForm):
    content = StringField('Treść',
                            validators=[DataRequired(), Length(min=3, max=300)])
    submit = SubmitField('Dodaj komentarz')