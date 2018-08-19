from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.crm import bp

@bp.route('/')
def all():
    return render_template('crm/index.html', title='Dashboard')
