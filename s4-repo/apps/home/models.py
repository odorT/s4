# -*- encoding: utf-8 -*-

from flask_login import UserMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass

class Databases(db.Model, UserMixin):

    __tablename__ = 'Databases'

    id = db.Column(db.Integer, primary_key=True)
    instance_id = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    capacity = db.Column(db.String(64))
    database = db.Column(db.String(64))
    user_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.instance_id)


# @login_manager.user_loader
# def user_loader(id):
#     return Users.query.filter_by(id=id).first()


# @login_manager.request_loader
# def request_loader(request):
#     instance_id = request.form.get('instance_id')
#     instance = Users.query.filter_by(instance_id=instance_id).first()
#     return instance if instance else None
