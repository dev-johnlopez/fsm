from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.crm import bp
from app.crm.forms import ContactForm
from app.crm.models import Contact
from app.src.util import flashFormErrors

@bp.route('/')
def index():
    return render_template('crm/index.html', title='Dashboard')

@bp.route('/search')
def search():
    return render_template('crm/index.html', title='Dashboard')

@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact()
        form.populate_obj(obj=contact)
        db.session.add(contact)
        db.session.commit()
    elif len(form.errors):
        flashFormErrors(form)
    return render_template('crm/create.html', title='Dashboard', form=form)
