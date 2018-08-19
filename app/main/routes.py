from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.main import bp
from app.main.forms import SearchForm
from app.crm.models import Contact

@bp.before_app_request
def before_request():
    g.search_form = SearchForm()

@bp.route('/')
def index():
    return render_template('main/index.html', title='Dashboard')

@bp.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    contacts, total = Contact.search(g.search_form.q.data, page, 20)
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * 20 else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('main/search.html', title='Search', contacts=contacts,
                           next_url=next_url, prev_url=prev_url)
