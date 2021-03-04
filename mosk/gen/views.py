from flask import Flask, Blueprint, render_template
from .. import log
from ..models import User
from . import gen

@gen.route('/')
def home():
    return render_template('home.html', users=User.objects, log=log)
