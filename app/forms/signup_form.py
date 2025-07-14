from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class SignupForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Sign Up")