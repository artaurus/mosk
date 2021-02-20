from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
import json

app = Flask(__name__)
with open('secrets.json', 'r') as file:
    secrets = json.loads(file.read())
    app.config['SECRET_KEY'] = secrets['SECRET_KEY']
    app.config['MONGO_URI'] = secrets['MONGO_URI']
mongo = PyMongo(app)

@app.route('/')
def home():
    users = mongo.db.users.find()
    return render_template('home.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mongo.db.users.insert_one({
            'name': name,
            'email': email
        })
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        email = request.form.get('email')
        mongo.db.users.delete_one({'email': email})
        return redirect(url_for('home'))
    return render_template('remove.html')

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    if request.method == 'POST':
        email = request.form.get('email')
        user = mongo.db.users.find_one({'email': email})
        if user:
            return redirect(url_for('modify_user', user=user['name']))
        else:
            return redirect(url_for('home'))
    return render_template('modify.html')

@app.route('/modify/<string:user>', methods=['GET', 'POST'])
def modify_user(user):
    if request.method == 'POST':
        name = request.form.get('name')
        mongo.db.users.update_one({'name': user},
        {'$set': {'name': name}})
        return redirect(url_for('home'))
    return render_template('modify_user.html', user=user)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
