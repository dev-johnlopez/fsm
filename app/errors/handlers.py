from app import app, db
from app.crm import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@bp.errorhandler(403)
def page_forbiden(error):
    return redirect(url_for_security("login"))
    
@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
