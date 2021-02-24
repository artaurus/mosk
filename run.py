from flask import Flask, render_template, redirect, request, url_for
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
from config import Config
from models import User

from flask import jsonify

# convert from module to package
# convert from package to app factory

db = MongoEngine()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
UserForm = model_form(User)

@app.route('/')
def home():
    return render_template('home.html', users=User.objects)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            User(name=form.name, email=form.email).save()
            return redirect(url_for('home'))
        except:
            return redirect(url_for('add'))
    return render_template('add.html', form=form)

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            User.objects(email=email).first().delete()
            return redirect(url_for('home'))
        except:
            return redirect(url_for('remove'))
    return render_template('remove.html')

# reduce modify algorithm to one view

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.objects(email=email).first()
        if user:
            return redirect(url_for('modify_user', user=user.name))
        else:
            return redirect(url_for('modify'))
    return render_template('modify.html')

@app.route('/modify/<string:user>', methods=['GET', 'POST'])
def modify_user(user):
    if request.method == 'POST':
        name = request.form.get('name')
        user = User.objects(name=user).first()
        user.name = name
        user.save()
        return redirect(url_for('home'))
    return render_template('modify_user.html', user=user)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
