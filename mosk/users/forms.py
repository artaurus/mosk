from wtforms import Form, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo, ValidationError
from ..models import User
from .. import log

class Unique:
    def __init__(self, model, message=None):
        self.model = model
        self.message = message if message else 'Already exists in the database.'

    def __call__(self, form, field):
        if self.model.objects(__raw__={field.name: field.data}).first():
            if log.status() and field.data == log.get_user()['email']:
                pass
            else:
                raise ValidationError(self.message)

class SignUpForm(Form):
    name = StringField(label='Name', validators=[InputRequired(), Length(min=3, max=25), Regexp('^[a-zA-Z]+( ?-?[a-zA-Z]+)*$')])
    email = StringField(label='Email', validators=[Email(), InputRequired(), Length(min=3, max=40), Unique(User)])
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=3, max=20), Regexp('^[a-zA-Z0-9_]+$')])
    confirm_password = PasswordField(label='Confirm password', validators=[EqualTo('password')])

class LoginForm(Form):
    email = StringField(label='Email', validators=[Email(), InputRequired(), Length(min=3, max=40)])
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=3, max=20), Regexp('^[a-zA-Z0-9_]+$')])

class ModifyProfileForm(Form):
    name = StringField(label='Name', validators=[InputRequired(), Length(min=3, max=25), Regexp('^[a-zA-Z]+( ?-?[a-zA-Z]+)*$')])
    email = StringField(label='Email', validators=[Email(), InputRequired(), Length(min=3, max=40), Unique(User)])
