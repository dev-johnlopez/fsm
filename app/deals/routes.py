from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.deals import bp
from app.deals.forms import SearchForm, DealForm
from app.deals.models import Deal, DealContact, DealContactRole, Property, Address
from app.crm.models import Contact
from sqlalchemy.orm import join

@bp.route('/')
def index():
    return render_template('deals/index.html', title='Dashboard')

@bp.route('/create')
def create():
    form = DealForm()
    return render_template('deals/create.html', title='Create', form=form)

@bp.route('/<deal_id>')
def view(deal_id):
    return render_template('deals/index.html', title='View')

@bp.route('/<deal_id>/edit')
def edit(deal_id):
    return render_template('deals/index.html', title='Edit')

@bp.route('/<deal_id>/delete')
def delete(deal_id):
    return render_template('deals/index.html', title='View')

@bp.route('/search', methods=['GET','POST'])
def search():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = Deal.query.join(Property).join(Address)
        if form.line_1.data:
            query = query.filter(Address.line_1.like('%' + form.line_1.data + '%'))
        if form.city.data:
            query = query.filter(Address.city.like('%' + form.city.data + '%'))
        if form.state_province.data:
            query = query.filter(Address.state_province.like('%' + form.state_province.data + '%'))
        if form.postal_code.data:
            query = query.filter(Address.postal_code.like('%' + form.postal_code.data + '%'))
        if form.name.data:
            query = query.join(DealContact).join(Contact).filter(Contact.name.like('%' + form.name.data + '%'))
        results = query.all()
        if len(results) == 0:
            flash('No results found.', 'info')
    else:
        for error in form.errors:
            flash(''.format(error), 'error')

    return render_template('deals/search.html', title='Search', results=results, form=form)
