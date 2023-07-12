from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models import model_recipes, model_notes

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/recipes/create', methods=['post'])
def create_recipes():
    
    is_valid = model_recipes.Recipe.validator(request.form)
    print(is_valid)

    if is_valid == False:
        return redirect('/')

    hash_pw = bcrypt.generate_password_hash(request.form['pw'])

    data = {
        **request.form,
        'pw': hash_pw
    }

    new_user = model_recipes.Recipe.create(data)
    print(new_user)

    session['uuid'] = new_user

    return redirect('/success')


@app.route('/recipes/login', methods=['post'])
def login():
    is_valid = model_recipes.Recipe.validator_login(request.form)

    if not is_valid:
        return redirect('/')

    return redirect('/')

@app.route('/success') #dashboard
def successful_login():
    
    if 'uuid' not in session:
        return redirect('/')


    # to add the name of user/recipe in the page when logged in
    id = session['uuid']
    user = model_recipes.Recipe.get_one({'id': id})
    all_notes = model_notes.Note.get_all()

    return render_template('/success.html', user = user, all_notes = all_notes)

@app.route('/recipes/logout')
def recipes_logout():
    
    del session['uuid']
    return redirect('/')