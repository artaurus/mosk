from flask import Flask, Blueprint, render_template, request
from mosk import um
from mosk.gen import gen

@gen.route('/')
def home():
    return render_template(
        '_base.html',
        um=um
    )
