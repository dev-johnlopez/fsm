from flask import g, render_template, flash, redirect, url_for, request
from app import db
from app.upload import bp
from app.upload.forms import UploadForm
from app.src.util.excel.excel_import import ExcelReader
from flask_security import login_required

@bp.route('/', methods=['GET','POST'])
@login_required
def index():
    form = UploadForm()
    if form.validate_on_submit():
        excelReader = ExcelReader()
        excelReader.readExcel(form.file.data)
    return render_template('upload/index.html', title='Upload', form=form)
