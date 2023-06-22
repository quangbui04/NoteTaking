from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
from website import db
import json
# Blueprint means that this file store all the roots

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) # URL to get to this endpoint
@login_required
# Whenever we enter the route above, home() is going to run
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category="success")
    return render_template("home.html", user=current_user)
    # we can reference in our template whether this current user is logged in

@views.route('/delete-note', methods=['POST'])
def delete_note():
    #load the data of the note we want to delete, its not in request form so we have to do this
    note = json.loads(request.data) # This is a dictionary
    noteId = note['noteId'] # Get note id
    note = Note.query.get(noteId) 
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
        