from flask import g, render_template, flash, redirect, url_for, request
from app import db
from flask_security import current_user
from app.crm import bp
from app.crm.forms import ContactForm, InvestmentCriteriaForm, SearchForm, InvestmentLocationForm
from app.crm.models import Contact, InvestmentCriteria, LocationCriteria
from app.src.util import flashFormErrors
from flask_security import login_required

@bp.route('/')
@login_required
def index():
    return render_template('crm/index.html', title='Dashboard')

@bp.route('/search', methods=['GET','POST'])
@login_required
def search():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = Contact.query.filter_by(user_id=current_user.id)
        if form.first_name.data:
            query = query.filter(Contact.first_name.like('%' + form.first_name.data + '%'))
        if form.last_name.data:
            query = query.filter(Contact.last_name.like('%' + form.last_name.data + '%'))
        results = query.all()
        if len(results) == 0:
            flash('No results found.', 'info')
    else:
        flashFormErrors(form)

    return render_template('crm/search.html', title='Search', form=form, results=results)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact()
        criteria = []
        for form_criteria in form.investment_criteria:
            if form_criteria.enabled.data:
                criteria.append(form_criteria)
        form.investment_criteria = criteria
        contact.investment_criteria = []
        form.populate_obj(obj=contact)
        current_user.contacts.append(contact)
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('crm.view', contact_id=contact.id))
    elif len(form.errors):
        flashFormErrors(form)
    return render_template('crm/create.html', title='Dashboard', form=form)

@bp.route('/edit/<contact_id>', methods=['GET','POST'])
@login_required
def edit(contact_id):
    return render_template('crm/index.html', title='Search', form=form, results=results)

@bp.route('/view/<contact_id>', methods=['GET', 'POST'])
@login_required
def view(contact_id):
    contact = Contact.query.get(contact_id)
    return render_template('crm/criteria.html', title='Criteria', contact=contact)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    contact = Contact.query.get(current_user.id)
    return render_template('crm/view.html', title='View Contact', contact=contact)

@bp.route('/<contact_id>/delete')
@login_required
def delete(contact_id):
    return render_template('crm/index.html', title='View')

@bp.route('/<contact_id>/criteria')
@login_required
def criteria(contact_id):
    contact = Contact.query.get(contact_id)
    return render_template('crm/criteria.html', title='Criteria', contact=contact)

@bp.route('/<contact_id>/criteria/create', methods=['GET','POST'])
@login_required
def add_criteria(contact_id):
    form = InvestmentCriteriaForm()
    if form.validate_on_submit():
        contact = Contact.query.get(contact_id)
        criteria = InvestmentCriteria()
        form.populate_obj(obj=criteria)
        contact.investment_criteria.append(criteria)
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('crm.criteria', contact_id=contact.id))
    elif len(form.errors):
        flashFormErrors(form)
    return render_template('crm/modify_criteria.html', title='Criteria', form=form)

@bp.route('/criteria/<criteria_id>/edit', methods=['GET','POST'])
@login_required
def edit_criteria(criteria_id):
    form = InvestmentCriteriaForm()
    return render_template('crm/modify_criteria.html', title='Criteria', form=form)
