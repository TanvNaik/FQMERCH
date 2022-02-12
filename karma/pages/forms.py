from flask_wtf import FlaskForm
from wtforms.validators import  DataRequired, EqualTo
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from flask_wtf.file import FileField, FileAllowed


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

class ProductForm(FlaskForm):

    producttype = StringField("type", validators=[dr], render_kw={"placeholder":"Product Type(hoodie/tshirt)"})
    productname = StringField("name", validators=[dr], render_kw={"placeholder":"Product Name"})
    price = IntegerField("Price", validators=[dr], render_kw={"placeholder":"Product Price"})
    originalprice = IntegerField("originalprice", validators=[dr], render_kw={"placeholder":"Product Original Price"})
    stock = IntegerField("stock", validators=[dr], render_kw={"placeholder":"Product Stock"})
    brand = StringField("brand", validators=[dr], render_kw={"placeholder":"Product Brand"})
    color = StringField("color", validators=[dr], render_kw={"placeholder":"Product Color"})
    image = FileField('Product Image', validators=[dr, FileAllowed(['jpg', 'png', 'jpeg'])])
    productcategory = StringField("category", validators=[dr], render_kw={"placeholder":"Product Category"})
    submit = SubmitField("Add Product")
