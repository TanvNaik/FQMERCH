from flask_wtf import FlaskForm
from wtforms.validators import  DataRequired, EqualTo
from wtforms import StringField, SubmitField, PasswordField


dr = DataRequired()

class LoginForm(FlaskForm):

    email = StringField("Email", validators=[dr], render_kw={"placeholder":"Email"})
    password = StringField("Password", validators=[dr], render_kw={"placeholder":"Confirm Password"})
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):

    username = StringField("Username", validators=[dr], render_kw={"placeholder":"Username"})
    email = StringField("Email", validators=[dr], render_kw={"placeholder":"Email"})
    password = StringField("Password", validators=[dr, EqualTo('confirmpassword', message='Password Must Match')], render_kw={"placeholder":"Password"})
    confirmpassword = StringField("Confirm Password", validators=[dr], render_kw={"placeholder":"Confirm Password"})
    submit = SubmitField("Register")
