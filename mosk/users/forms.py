from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, Email, Regexp, EqualTo, ValidationError
from mosk import um
from mosk.users.models import User

def input_required(form, field):
    if len(field.data) == 0:
        raise ValidationError('')

def unique(form, field):
    if User.objects(email=field.data).first():
        if um.status() and field.data == um.get_user('email'):
            pass
        else:
            raise ValidationError('Already exists in our database.')

def not_registered(form, field):
    if not User.objects(email=field.data).first():
        raise ValidationError('Does not exist in our database.')

class SignUpForm(Form):
    email = StringField(label='Email address', validators=[input_required, unique, Length(min=5, max=254), Regexp('^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$')])
    password = PasswordField(label='Password', validators=[input_required, Length(min=8, max=20), Regexp('^[a-zA-Z0-9_]+$')])
    confirm_password = PasswordField(label='Confirm password', validators=[EqualTo('password')])

class LoginForm(Form):
    email = StringField(label='Email address', validators=[input_required, not_registered, Length(min=5, max=254), Regexp('^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$')])
    password = PasswordField(label='Password', validators=[input_required, Length(min=8, max=20), Regexp('^[a-zA-Z0-9_]+$')])

class EditProfileForm(Form):
    email = StringField(label='Email address', validators=[input_required, unique, Length(min=5, max=254), Regexp('^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$')])

class EmailForm(Form):
    email = StringField(label='Email address', validators=[input_required, not_registered, Length(min=5, max=254), Regexp('^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]+$')])

class ResetPasswordForm(Form):
    password = PasswordField(label='New password', validators=[input_required, Length(min=8, max=20), Regexp('^[a-zA-Z0-9_]+$')])
    confirm_password = PasswordField(label='Confirm password', validators=[EqualTo('password')])
