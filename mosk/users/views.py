from flask import Flask, render_template, redirect, request, url_for, abort
from flask_mongoengine.wtf import model_form
from werkzeug.routing import BuildError
import re
from .. import db, log
from ..models import User
from . import users
from .forms import SignUpForm, LoginForm, ModifyProfileForm

@users.route('/sign-up', methods=['GET', 'POST'])
@log.access_denied
def sign_up():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(name=form.name.data, email=form.email.data, password=log.encrypt(form.password.data))
        user.save()
        log.set_user(user)
        return redirect(url_for('gen.home'))
    return render_template('sign_up.html', title='Sign Up', form=form)

@users.route('/login', methods=['GET', 'POST'])
@log.access_denied
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects(email=form.email.data).first()
        if user:
            log.authenticate(user, form.password.data)
            next = request.args.get('next')
            if next and re.search('^[a-z]+(_?[a-z]+)*$', next):
                try:
                    url = url_for('users.'+next)
                except BuildError:
                    abort(404)
                return redirect(url)
            return redirect(url_for('gen.home'))
        else:
            return redirect(url_for('users.login'))
    return render_template('login.html', title='Login', form=form)

@users.route('/profile', methods=['GET', 'POST'])
@log.access_required
def profile():
    return render_template('profile.html', title='Profile', log=log)

@users.route('/profile/modify', methods=['GET', 'POST'])
@log.access_required
def modify_profile():
    form = ModifyProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects(email=log.get_user()['email']).first()
        user.name = form.name.data
        user.email = form.email.data
        user.save()
        log.reset_user()
        log.set_user(user)
        return redirect(url_for('users.profile'))
    return render_template('modify_profile.html', title='Modify Profile', form=form, log=log)

@users.route('/logout')
@log.access_required
def logout():
    log.reset_user()
    return redirect(url_for('gen.home'))

@users.route('/profile/delete')
@log.access_required
def delete():
    User.objects(email=log.get_user()['email']).first().delete()
    return redirect(url_for('users.logout'))
