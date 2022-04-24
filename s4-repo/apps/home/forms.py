# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class DatabaseForm(FlaskForm):
    instance_id = StringField('instance_id',
        id='instance_id',
        validators=[DataRequired()]
    )

    password = PasswordField('password',
        id='password',
        validators=[DataRequired()]
    )

    capacity = IntegerField('capacity',
        id='capacity',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=65536)
        ]
    )