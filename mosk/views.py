from flask import Flask, render_template, redirect, request, url_for
from flask_mongoengine.wtf import model_form
from werkzeug.routing import BuildError
from mongoengine.errors import NotUniqueError
from mosk import app, db, log
from mosk.models import User
from mosk.forms import SignUp, Login, ModifyProfile
import re

signup_form = model_form(SignUp, field_args={'password': {'password': True}})
login_form = model_form(Login, field_args={'password': {'password': True}})
modify_form = model_form(ModifyProfile)

@app.route('/')
def home():
    # add search bar
    # paginate queryset
    return render_template('home.html', users=User.objects, log=log)

@app.route('/sign_up', methods=['GET', 'POST'])
@log.access_denied
def sign_up():
    form = signup_form(request.form)
    if request.method == 'POST' and form.validate():
        user = User(name=form.name.data, email=form.email.data, password=log.encrypt(form.password.data))
        try:
            user.save()
        except NotUniqueError:
            return redirect(url_for('sign_up'))
        log.set_user(user)
        return redirect(url_for('home'))
    return render_template('sign_up.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
@log.access_denied
def login():
    form = login_form(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects(email=form.email.data).first()
        if user:
            log.authenticate(user, form.password.data)
            next = request.args.get('next')
            if next and bool(re.search('[a-z]+_?[a-z]*', next)):
                try:
                    url = url_for(next)
                except BuildError:
                    url = url_for('home')
                return redirect(url)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@log.access_required
def profile():
    return render_template('profile.html', log=log)

@app.route('/modify', methods=['GET', 'POST'])
@log.access_required
def modify():
    form = modify_form(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects(email=log.get_user()['email']).first()
        user.name = form.name.data
        user.email = form.email.data
        try:
            user.save()
        except NotUniqueError:
            return redirect(url_for('modify'))
        log.reset_user()
        log.set_user(user)
        return redirect(url_for('profile'))
    return render_template('modify.html', form=form, log=log)

@app.route('/logout')
@log.access_required
def logout():
    log.reset_user()
    return redirect(url_for('home'))

@app.route('/delete')
@log.access_required
def delete():
    User.objects(email=log.get_user()['email']).first().delete()
    return redirect(url_for('logout'))
