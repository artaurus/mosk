from flask import Flask, Blueprint, render_template, request
from .. import log
from ..models import User
from . import gen

@gen.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    users = User.objects.paginate(page=page, per_page=8)
    return render_template('home.html', users=users, log=log)
