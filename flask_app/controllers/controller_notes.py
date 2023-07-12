from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models import model_recipes, model_notes

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/notes/new')
def new_notes():

    return render_template('notes_new.html')

@app.route('/notes/create', methods=['post'])
def create_notes():

    #process validators
    is_valid = model_notes.Note.validator(request.form)

    if not is_valid:
        return redirect('/notes/new')

    return redirect('/success')

@app.route('/notes/<int:id>/edit')
def notes_edit(id):
    note = model_notes.Note.get_one({'id': id})

    return render_template('notes_edit.html', note = note)


@app.route('/notes/<int:id>/update', methods=['post'])
def notes_update(id):
    is_valid = model_notes.Note.validator(request.form)

    if not is_valid:
        return redirect(f'/notes/{id}/edit')

    return redirect('/success')


@app.route('/notes/<int:id>/view')
def notes_view_instructions(id):

    user = model_recipes.Recipe.get_one({'id': session['uuid']})
    recipe = model_notes.Note.get_one({'id': id})


    return render_template('notes_view_instr.html', user = user, recipe = recipe)

@app.route('/notes/<int:id>/delete')
def notes_delete(id):
    model_notes.Note.delete_one({'id': id})
    return redirect('/success')