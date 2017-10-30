from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField  # validators
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired(),
                           Length(min=4, max=25)])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired(),
                           Length(min=4, max=25)])
    password = PasswordField('password', validators=[DataRequired(),
                             EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])  # length?
