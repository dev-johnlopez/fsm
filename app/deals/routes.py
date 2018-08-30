from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.deals import bp
from app.deals.forms import SearchForm, DealForm, PropertyForm, MarketDealForm
from app.deals.models import Deal, Property, Address
from app.crm.models import Contact
from app.src.util import flashFormErrors
from sqlalchemy.orm import join
from flask_security import login_required

@bp.route('/')
@login_required
def index():
    return render_template('deals/index.html', title='Dashboard')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = DealForm()
    if form.validate_on_submit():
        deal = Deal()
        deal.property = Property()
        deal.property.address = Address()
        form.populate_obj(deal)
        db.session.add(deal)
        db.session.commit()
        return redirect(url_for('deals.view', deal_id=deal.id))
    elif len(form.errors):
        flashFormErrors(form)
    return render_template('deals/create.html', title='Create', form=form)

@bp.route('/<deal_id>', methods=['GET', 'POST'])
@login_required
def view(deal_id):
    deal = Deal.query.get(deal_id)
    form = DealForm(obj=deal)
    if form.validate_on_submit():
        form.populate_obj(deal)
        db.session.add(deal)
        db.session.commit()
        flash('Your updates have been saved.', 'info')
    elif len(form.errors):
        flashFormErrors(form)
    return render_template('deals/view.html', title='View', deal=deal, form=form)

@bp.route('/<deal_id>/email', methods=['GET', 'POST'])
@login_required
def email(deal_id):
    deal = Deal.query.get(deal_id)
    form = MarketDealForm()
    if form.validate_on_submit():
        flash(form.body.data, 'info')
    elif len(form.errors):
        flashFormErrors(form)
    return render_template('deals/email.html', title='Email', deal=deal, form=form)

@bp.route('/<deal_id>/edit')
@login_required
def edit(deal_id):
    deal = Deal.query.get(deal_id)
    form = DealForm(obj=deal)
    if form.validate_on_submit():
        form.populate_obj(deal)
        db.session.add(deal)
        db.session.commit()
        return redirect(url_for('deals.summary', deal_id=deal.id))
    elif len(form.errors):
        flashFormErrors(form)
    return render_template('deals/create.html', title='Create', form=form, deal=deal)

@bp.route('/<deal_id>/delete')
@login_required
def delete(deal_id):
    return render_template('deals/index.html', title='View')

@bp.route('/search', methods=['GET','POST'])
@login_required
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
        results = query.all()
        if len(results) == 0:
            flash('No results found.', 'info')
    else:
        flashFormErrors(form)

    return render_template('deals/search.html', title='Search', results=results, form=form)
