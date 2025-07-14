from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, IntegerField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

TIMEZONE_CHOICES = [
    ("Etc/UTC", "UTC"),
    ("Pacific/Honolulu", "Pacific - Honolulu"),
    ("America/Anchorage", "America - Anchorage"),
    ("America/Los_Angeles", "America - Los Angeles"),
    ("America/Denver", "America - Denver"),
    ("America/Chicago", "America - Chicago"),
    ("America/New_York", "America - New York"),
    ("America/Toronto", "America - Toronto"),
    ("America/Mexico_City", "America - Mexico City"),
    ("America/Bogota", "America - Bogota"),
    ("America/Lima", "America - Lima"),
    ("America/Santiago", "America - Santiago"),
    ("America/Sao_Paulo", "America - Sao Paulo"),
    ("America/Argentina/Buenos_Aires", "America - Buenos Aires"),
    ("Europe/London", "Europe - London"),
    ("Europe/Dublin", "Europe - Dublin"),
    ("Europe/Paris", "Europe - Paris"),
    ("Europe/Berlin", "Europe - Berlin"),
    ("Europe/Madrid", "Europe - Madrid"),
    ("Europe/Rome", "Europe - Rome"),
    ("Europe/Amsterdam", "Europe - Amsterdam"),
    ("Europe/Stockholm", "Europe - Stockholm"),
    ("Europe/Zurich", "Europe - Zurich"),
    ("Europe/Prague", "Europe - Prague"),
    ("Europe/Athens", "Europe - Athens"),
    ("Europe/Moscow", "Europe - Moscow"),
    ("Africa/Cairo", "Africa - Cairo"),
    ("Africa/Nairobi", "Africa - Nairobi"),
    ("Africa/Johannesburg", "Africa - Johannesburg"),
    ("Asia/Jerusalem", "Asia - Jerusalem"),
    ("Asia/Dubai", "Asia - Dubai"),
    ("Asia/Karachi", "Asia - Karachi"),
    ("Asia/Kolkata", "Asia - Kolkata"),
    ("Asia/Dhaka", "Asia - Dhaka"),
    ("Asia/Bangkok", "Asia - Bangkok"),
    ("Asia/Jakarta", "Asia - Jakarta"),
    ("Asia/Singapore", "Asia - Singapore"),
    ("Asia/Kuala_Lumpur", "Asia - Kuala Lumpur"),
    ("Asia/Manila", "Asia - Manila"),
    ("Asia/Hong_Kong", "Asia - Hong Kong"),
    ("Asia/Shanghai", "Asia - Shanghai"),
    ("Asia/Taipei", "Asia - Taipei"),
    ("Asia/Seoul", "Asia - Seoul"),
    ("Asia/Tokyo", "Asia - Tokyo"),
    ("Australia/Perth", "Australia - Perth"),
    ("Australia/Adelaide", "Australia - Adelaide"),
    ("Australia/Brisbane", "Australia - Brisbane"),
    ("Australia/Melbourne", "Australia - Melbourne"),
    ("Australia/Sydney", "Australia - Sydney"),
    ("Pacific/Auckland", "Pacific - Auckland")
]

class SettingsForm(FlaskForm):
    reminder_activate = BooleanField("Activate Reminder")
    reminder_timezone = SelectField("Reminder Timezone", choices=TIMEZONE_CHOICES, validators=[DataRequired()])
    reminder_offset = SelectField("Reminder Timing", choices=[("1", "1 day before"), ("0", "Same day")], validators=[DataRequired()])
    reminder_hour = IntegerField("Reminder Hour (0-23)", validators=[DataRequired(), NumberRange(min=0, max=23)])
    email_subject = StringField("Email Subject", validators=[DataRequired(), Length(max=255)])
    email_body = TextAreaField("Email Body", validators=[DataRequired()])
    submit = SubmitField("Save")