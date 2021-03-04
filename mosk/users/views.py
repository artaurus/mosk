from flask import Flask, Blueprint, render_template, redirect, request, url_for
from flask_mongoengine.wtf import model_form
from werkzeug.routing import BuildError
from mongoengine.errors import NotUniqueError
import re
from .. import db, log
from ..models import User
from . import users
from .forms import SignUp, Login, ModifyProfile

@users.route('/sign-up', methods=['GET', 'POST'])
@log.access_denied
def sign_up():
    signup_form = model_form(SignUp, field_args={'password': {'password': True}})
    form = signup_form(request.form)
    if request.method == 'POST' and form.validate():
        user = User(name=form.name.data, email=form.email.data, password=log.encrypt(form.password.data))
        try:
            user.save()
        except NotUniqueError:
            return redirect(url_for('users.sign_up'))
        log.set_user(user)
        return redirect(url_for('gen.home'))
    return render_template('sign_up.html', title='Sign Up', form=form)

@users.route('/login', methods=['GET', 'POST'])
@log.access_denied
def login():
    login_form = model_form(Login, field_args={'password': {'password': True}})
    form = login_form(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects(email=form.email.data).first()
        if user:
            log.authenticate(user, form.password.data)
            next = request.args.get('next')
            if next and re.search('^[a-z]+(_?[a-z]+)*$', next):
                try:
                    # needs fixing for more blueprints
                    url = url_for('users.'+next)
                except BuildError:
                    url = url_for('gen.home')
                return redirect(url)
            return redirect(url_for('gen.home'))
        else:
            return redirect(url_for('users.login'))
    return render_template('login.html', title='Login', form=form)

@users.route('/profile', methods=['GET', 'POST'])
@log.access_required
def profile():
    return render_template('profile.html', title='Profile', log=log)

@users.route('/modify', methods=['GET', 'POST'])
@log.access_required
def modify():
    modify_form = model_form(ModifyProfile)
    form = modify_form(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects(email=log.get_user()['email']).first()
        user.name = form.name.data
        user.email = form.email.data
        try:
            user.save()
        except NotUniqueError:
            return redirect(url_for('users.modify'))
        log.reset_user()
        log.set_user(user)
        return redirect(url_for('users.profile'))
    return render_template('modify.html', title='Modify Profile', form=form, log=log)

@users.route('/logout')
@log.access_required
def logout():
    log.reset_user()
    return redirect(url_for('gen.home'))

@users.route('/delete')
@log.access_required
def delete():
    User.objects(email=log.get_user()['email']).first().delete()
    return redirect(url_for('users.logout'))
