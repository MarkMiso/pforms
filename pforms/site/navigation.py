from flask import Blueprint, render_template, redirect, url_for, request, flash

navigation = Blueprint('navigation', __name__)

@navigation.route('/')
def index():
    return render_template("index.html")