from flask import Flask, render_template, redirect, request, url_for
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
from config import Config
from models import User

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
        User(name=form.name.data, email=form.email.data).save()
        return redirect(url_for('home'))
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

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects(email=form.email.data).first()
        user.name = form.name.data
        user.save()
        return redirect(url_for('home'))
    return render_template('modify.html', form=form)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
