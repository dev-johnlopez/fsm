from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.deals import bp

@bp.route('/')
def all():
    return render_template('deals/index.html', title='Dashboard')

@bp.route('/<deal_id>')
def view(deal_id):
    return render_template('deals/all.html', title='Dashboard')
