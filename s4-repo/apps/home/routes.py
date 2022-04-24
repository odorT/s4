# -*- encoding: utf-8 -*-

from apps.home import blueprint

from jinja2 import TemplateNotFound
from flask import render_template, redirect, request, url_for
from flask_login import (
    login_required,
    current_user,
    login_user,
    logout_user
)
from apps import db
from apps.home.forms import DatabaseForm
from apps.home.models import Databases
from apps.home.provision import Provision


# Routes

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', segment='dashboard')


@blueprint.route('/databases', methods=['GET', 'POST'])
@login_required
def databases():
    if request.method == 'POST':
        id = list(request.form.keys())[0]
        provisioner = Provision(id)
        provisioner.destroy()
    
    instances = []
    instance_infos = []

    databases = Databases.query.filter_by(user_id=current_user.id).all()
    for database in databases:
        instances.append(database.instance_id)
    
    if len(instances) == 0:
        return render_template('home/databases.html',
            msg="No database instance",
            success=True
        )

    for instance_id in instances:
        try:
            provisioner = Provision(instance_id)
            instance_infos.append(provisioner.get_info())
        except:
            continue
    
    print(instance_infos)

    return render_template('home/databases.html',
        success=True,
        instance_infos=instance_infos
    )

@blueprint.route('/create_database', methods=['GET', 'POST'])
@login_required
def create_database():
    database_form = DatabaseForm(request.form)

    if 'instance_id' in request.form:
        instance_id = request.form['instance_id']

        instance = Databases.query.filter_by(instance_id=instance_id).first()
        if instance:
            return render_template('home/create-database.html',
                msg=f"Instance with id {instance_id} already exists or it has been deleted in the recent past",
                success=False,
                form=database_form
            )

        sql_instance = Provision(instance_id=instance_id)
        sql_instance.create(password=request.form['password'], capacity=request.form['capacity'], database_type=request.form['database'])
        
        session_form = {
            "user_id": current_user.id
        }
        session_form.update(request.form)

        database = Databases(**session_form)
        db.session.add(database)
        db.session.commit()

        return render_template('home/create-database.html',
            msg="Database initialization started, please wait a few minutes while we provision your database",
            success=True,
            form=database_form
        )
    else:
        return render_template('home/create-database.html', form=database_form)


@blueprint.route('/transactions')
@login_required
def transactions():
    return render_template('home/transactions.html', segment='transactions')


@blueprint.route('/settings')
@login_required
def settings():
    return render_template('home/settings.html', segment='settings')


@blueprint.route('/keyfile', methods=['GET', 'POST'])
@login_required
def keyfile():
    print(request.form)
    return "Successful upload"

