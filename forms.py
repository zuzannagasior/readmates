from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
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