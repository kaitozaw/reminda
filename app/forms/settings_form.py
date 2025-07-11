from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Email, Optional, Length

class SettingsForm(FlaskForm):
    reminder_offset = SelectField("Reminder Timing", choices=[("1", "1 day before"), ("0", "Same day")], validators=[DataRequired()])
    reminder_hour = IntegerField("Reminder Hour (0-23)", validators=[DataRequired(), NumberRange(min=0, max=23)])
    email_subject = StringField("Email Subject", validators=[DataRequired(), Length(max=255)])
    email_body = TextAreaField("Email Body", validators=[DataRequired()])
    submit = SubmitField("Save")