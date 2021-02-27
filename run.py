from flask import Flask, render_template, redirect, request, url_for
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
from mongoengine.errors import NotUniqueError
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from login import LoginHandler
from models import User, Login, ModifyProfile

db = MongoEngine()
log = LoginHandler()
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

user_form = model_form(User, field_args={'password': {'password': True}})
login_form = model_form(Login, field_args={'password': {'password': True}})
modify_form = model_form(ModifyProfile)

@app.route('/')
def home():
    # paginate queryset
    return render_template('home.html', users=User.objects, log=log)

@app.route('/sign_up', methods=['GET', 'POST'])
@log.access_denied
def sign_up():
    form = user_form(request.form)
    if request.method == 'POST' and form.validate():
        hashed = generate_password_hash(form.password.data, method='sha256')
        user = User(name=form.name.data, email=form.email.data, password=hashed)
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
        if user and check_password_hash(user['password'], form.password.data):
            log.set_user(user)
            next = request.args.get('next')
            if next:
                return redirect(url_for(next))
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

if __name__ == '__main__':
    app.run(port=8000, debug=True)
