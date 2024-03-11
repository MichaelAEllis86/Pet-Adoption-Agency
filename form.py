from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired,Optional,NumberRange,URL, AnyOf


class AddPetForm(FlaskForm):
    """form model to add a new pet"""

    # email=StringField("Email", validators=[Email(message="hey hey hey u cant park here! no parking!")])
    name=StringField("Pet Name", validators=[InputRequired(message="This field is required, please add a pet name")])
    species=StringField("Species",validators=[InputRequired(message="This field is required, please choose a species"), AnyOf(values=["cat","dog","porcupine"],message="Species must be cat, dog, or porcupine. We are so VERY selective")])
    photo_url=StringField("Photo url",validators=[Optional(), URL(require_tld=False, message="please enter a valid URL for your pets photo")])
    age=IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=30, message="choose an age from zero to 30")])
    notes=StringField("Notes", validators=[Optional()])

class EditPetForm(FlaskForm):
    """form model to edit an existing pet"""
    photo_url=StringField("Photo url",validators=[Optional(), URL( message="please enter a valid URL for your pets photo")])
    notes=StringField("Notes", validators=[Optional()])
    is_available=BooleanField("Available for adoption")
