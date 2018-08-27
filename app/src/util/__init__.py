from flask import flash

def flashFormErrors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash('{}: {}'.format(getattr(form, field).label.text, error), 'error')
