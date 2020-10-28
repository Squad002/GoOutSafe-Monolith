from wtforms import widgets
from monolith.models.precautions import Precautions
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from monolith.app import db
import wtforms as f
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    password = f.PasswordField("password", validators=[DataRequired()])
    display = ["email", "password"]


class UserForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    firstname = f.StringField("firstname", validators=[DataRequired()])
    lastname = f.StringField("lastname", validators=[DataRequired()])
    password = f.PasswordField("password", validators=[DataRequired()])
    dateofbirth = f.DateField("dateofbirth", format="%d/%m/%Y")
    display = ["email", "firstname", "lastname", "password", "dateofbirth"]


# TODO Validators are missing?
class OperatorForm(UserForm):
    # TODO validate fiscal code in a good proper way
    fiscal_code = f.StringField("fiscalcode", validators=[DataRequired()])
    display = [
        "email",
        "firstname",
        "lastname",
        "password",
        "dateofbirth",
        "fiscal_code",
    ]


class AuthorityForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    name = f.StringField("name", validators=[DataRequired()])
    password = f.PasswordField("password", validators=[DataRequired()])
    phone = f.IntegerField("phone", validators=[DataRequired()])
    country = f.StringField("country", validators=[DataRequired()])
    state = f.StringField("state", validators=[DataRequired()])
    city = f.StringField("city", validators=[DataRequired()])
    lat = f.DecimalField("latitude", validators=[DataRequired()])
    lon = f.DecimalField("longitude", validators=[DataRequired()])

    display = ["email", "name", "password", "country", "state", "city", "lat", "lon"]


def precautions_choices():
    return db.session.query(Precautions)


class MultiCheckboxField(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CreateRestaurantForm(FlaskForm):
    name = f.StringField("name", validators=[DataRequired()])
    lon = f.FloatField("longitude", validators=[DataRequired()])
    lat = f.FloatField("latitude", validators=[DataRequired()])
    phone = f.IntegerField("phone", validators=[DataRequired()])
    prec_measures = MultiCheckboxField(
        "precautions",
        validators=[DataRequired()],
        get_label="name",
        query_factory=precautions_choices,
    )
    display = ["name", "lat", "lon", "phone", "prec_measures"]


class CreateTableForm(FlaskForm):
    name = f.StringField("name", validators=[DataRequired()])
    seats = f.IntegerField("seats", validators=[DataRequired()])
    display = ["name", "seats"]