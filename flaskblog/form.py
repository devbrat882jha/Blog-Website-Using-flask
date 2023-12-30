from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired, Email,Length,EqualTo,ValidationError
from flaskblog.models import User
from flask_login import current_user 
from flask_wtf.file import FileField,file_allowed

secret_key="47cbc83e5d0ca093b0f8fb560178904c"

#we have username templates in username variable,so for other variables, username as argument is label that user will see
class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=4,max=20)])#in list
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=4)])
    confirm_password=PasswordField('confirm_password',validators=[EqualTo('password')])
    submit=SubmitField('Sign up')
    def validate_username(self,username):#this is field #if condition mathces then it will raise error in form
        user=User.query.filter_by(username=username.data).first()#if username in database matches to username.data(in form)then user object is initialise
        if user:
            raise ValidationError("username already taken")#import validation error
    def validate_email(self,email):#if condition mathces then it will raise error in form
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("email already taken")
    
        


class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=4)])
    remember=BooleanField('Remember')
    submit=SubmitField('Login')

class UpdateForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=4,max=20)])#in list
    email=StringField('Email',validators=[DataRequired(),Email()])
    profile=FileField('change your profile picture',validators=[file_allowed(['jpg','jpeg','png'])])
   
    def validate_username(self,username):#this is field #if condition mathces then it will raise error in form
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first()#if username in database matches to username.data(in form)then user object is initialise
            if user:
                raise ValidationError("username already taken")#import validation error
    def validate_email(self,email):#if condition mathces then it will raise error in form
          if email.data!=current_user.email:
                user=User.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError("email already taken")
                

class PostForm(FlaskForm):
    title=StringField('title',validators=[DataRequired()])
    content=TextAreaField('content',validators=[DataRequired()])
    submit=SubmitField('create post')


class ResetForm(FlaskForm):
    
    email=StringField('Email',validators=[DataRequired(),Email()])
   
    submit=SubmitField('Request Reset')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("No email found.Please sign up first")
        

class PasswordReset(FlaskForm):
    password=PasswordField('password',validators=[DataRequired(),Length(min=4)])
    confirm_password=PasswordField('confirm_password',validators=[EqualTo('password')])
    submit=SubmitField('Reset password')
   

