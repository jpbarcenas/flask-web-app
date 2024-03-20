'''
Setup the standard routes for the website except the authentication routes
'''
from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import login_required, current_user
from . import db
from .models import Notes
import json

pages = Blueprint('pages', __name__)

@pages.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Handle the note form submission
        requestBody = request.form
        title = requestBody['title']
        content = requestBody['content']
        
        if len(title) < 1:
            flash("Title is too short!", category='error')
        elif len(title) > 150:
            flash("Title is too long!", category='error')
        elif len(content) < 1:
            flash("Note is too short!", category='error')
        elif len(content) > 10000:
            flash("Note is too long!", category='error')
        else:
            # Add the note to the database
            new_note = Notes(title=title, 
                             content=content, 
                             date=db.func.now(),
                             user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            
            flash("Note added!", category='success')

        return render_template("home.html", user=current_user)
    else:
        # retrieve the notes from the database
        notes = Notes.query.filter_by(user_id=current_user.id).all()

        # Display the home page
        return render_template("home.html", user=current_user)
    
@pages.route('/notes/delete', methods=['POST'])
@login_required
def delete_note():
    # Handle the note delete form submission
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Notes.query.get(note_id)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note deleted!", category='success')
        else:
            flash("You can only delete your own notes!", category='error')
    
    return jsonify({})