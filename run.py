from flask import Flask, render_template, redirect, request, url_for
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
import json

# convert from module to package
# convert from package to app factory

app = Flask(__name__)

# set up config file

with open('secrets.json', 'r') as file:
    secrets = json.loads(file.read())
    app.config['SECRET_KEY'] = secrets['SECRET_KEY']
    app.config['MONGODB_SETTINGS'] = {'host': secrets['MONGO_URI']}
db = MongoEngine(app)

# shift to models.py

class User(db.Document):
    name = db.StringField(required=True, min_length=4, max_length=20)
    email = db.EmailField(required=True, min_length=4, max_length=40)
    meta = {'collection': 'users'}

UserForm = model_form(User)

@app.route('/')
def home():
    return render_template('home.html', users=User.objects)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form.get('name')
        email = request.form.get('email')
        try:
            User(name=name, email=email).save()
        except:
            pass
        return redirect(url_for('home'))
    return render_template('add.html', form=form)

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            User.objects(email=email).delete()
        except:
            pass
        return redirect(url_for('home'))
    return render_template('remove.html')

# finish crud routes

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    if request.method == 'POST':
        email = request.form.get('email')

        if user:
            return redirect(url_for('modify_user', user=user['name']))
        else:
            return redirect(url_for('home'))
    return render_template('modify.html')

# @app.route('/modify/<string:user>', methods=['GET', 'POST'])
# def modify_user(user):
#     if request.method == 'POST':
#         name = request.form.get('name')
#
#         return redirect(url_for('home'))
#     return render_template('modify_user.html', user=user)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
