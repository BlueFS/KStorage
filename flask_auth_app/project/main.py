# Some of this knowledge was gained from Digital Ocean on how to create a login page.
# Specifically how to use Blueprint
from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory, abort, flash
from flask_login import login_required, current_user
from . import db
from .models import UploadedFile
import os

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    user_files = UploadedFile.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', name=current_user.name, files=user_files)


@main.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

# Used ChatGPT to get the format for some stuff inclulding abort and delete file


@main.route('/downloaded/<int:file_id>')
@login_required
def download_file(file_id):
    file = UploadedFile.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        abort(403)
    return send_from_directory(directory=os.path.dirname(file.filepath),
                               path=os.path.basename(file.filepath),
                               as_attachment=True)


@main.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file = UploadedFile.query.get_or_404(file_id)
    if file.user_id != current_user.id:
        abort(403)
    try:
        os.remove(file.filepath)
    except FileNotFoundError:
        # Avoids error if file is gone
        pass

    db.session.delete(file)
    db.session.commit()
    flash('File deleted successfully', 'success')
    return redirect(url_for('main.profile'))
