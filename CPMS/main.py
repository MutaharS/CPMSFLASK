from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import login_required, current_user
from flask import send_file, current_app as app

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import datetime
from .models import User, Paper
from . import db
import os, ntpath

# For opening tab
import webbrowser
new = 2 # open in a new tab, if possible

main = Blueprint('main', __name__)

# For identifying the allowed file extensions
ALLOWED_EXTENSIONS = {'pdf','dummy'}
UPLOAD_FOLDER = '/project/uploads' # config isn't working
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/profile')
@login_required
def profile():
    my_papers = Paper.query.filter_by(uid=current_user.uid).all()
    subtimes = [q.subtime for q in my_papers]
    paperpaths = [q.papername for q in my_papers]
    li = []
    for i in range(len(subtimes)):
        li.append([subtimes[i],paperpaths[i]])
    return render_template('profile.html', name=current_user.name, li=li)

@main.route('/openpdf/<path:papername>')
def openpdf(papername):
    return send_file('uploads/'+papername,attachment_filename=papername)
    #with open('project/uploads/'+papername, 'rb') as static_file:
    #    return send_file(static_file, attachment_filename=papername, )
    #return render_template('profile.html')

@main.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('main.profile',msg='file upload unsuccessful'))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('main.profile',msg='no file selected'))
        if file and allowed_file(file.filename):
            f = request.files['file']
            filename = secure_filename(f.filename)
            path = os.path.join("project","uploads",secure_filename(f.filename))
            papername = ntpath.basename(path)
            print('\n'+papername+'\n')
            # Insert paper into database
            dt = datetime.now().isoformat(timespec='minutes')
            new_paper = Paper(uid=current_user.uid, papername=papername,paperpath=path, author=current_user.name, subtime=dt)
            db.session.add(new_paper)
            db.session.commit()

            # Save the paper to local memory
            f.save(path)
            return redirect(url_for('main.profile',msg='file upload successful'))
    return render_template('profile.html')
