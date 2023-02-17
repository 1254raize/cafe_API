from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL


seats_options = ["0-10", "10-20", "20-30", "30-40", "40-50", "50+"]


class AddCafeForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    map_url = URLField(label="Map URL", validators=[DataRequired(), URL()])
    img_url = URLField(label="Image URL", validators=[DataRequired(), URL()])
    location = StringField(label="Location", validators=[DataRequired()])
    has_sockets = BooleanField(label="Has Sockets?")
    has_toilet = BooleanField(label="Has Toilet?")
    has_wifi = BooleanField(label="Has Wifi?")
    can_take_calls = BooleanField(label="Can take calls?")
    seats = SelectField('Number of seats', choices=seats_options, coerce=str, validators=[DataRequired()])
    coffee_price = StringField(label="Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Submit")
