from flask_wtf.file import FileAllowed, FileField
from wtforms import Form, StringField, PasswordField, validators, SubmitField, ValidationError
from flask_wtf import FlaskForm
from .models import Register


class CustomerRegisterForm(FlaskForm):
    firstname = StringField('First Name:', [validators.DataRequired()])
    lastname = StringField('Last Name:', [validators.DataRequired()])
    username = StringField('Username:', [validators.DataRequired()])
    email = StringField('Email:', [validators.Email(), validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match! '), validators.Length(min=6, max=25)])
    confirm = PasswordField('Confirm Password:', [validators.DataRequired()])
    city = StringField('City:', [validators.DataRequired()])
    country = StringField('Country:', [validators.DataRequired()])
    contact = StringField('Phone Number: ', [validators.DataRequired()])
    address = StringField('Address:', [validators.DataRequired()])

    profile = FileField('Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])

    submit = SubmitField('Register')


    def validate_user_name(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("Username already exists!")

    
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("Email address already exists!")


class CustomerLoginForm(FlaskForm):
    email = StringField('Email:', [validators.Email(), validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])