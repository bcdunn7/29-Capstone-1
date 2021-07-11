from flask_wtf import FlaskForm
from flask_wtf.csrf import _FlaskFormCSRF
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class UserForm(FlaskForm):
    """Form for adding or logging in users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters.")])
