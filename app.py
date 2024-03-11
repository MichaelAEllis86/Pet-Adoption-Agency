import os
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from flask_sqlalchemy import SQLAlchemy
from form import AddPetForm, EditPetForm
# from form import AddSnackForm

app=Flask(__name__)
app.app_context().push()

# set environment variable to NOTTEST if were working the real DB in app.py, if we are in test mode in test.py this variable is set to "TEST" and we use the test database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///pet_adoption_db' if os.environ.get("TEST", "NOTTEST") == "NOTTEST" else 'postgresql:///test_pet_adoption_db' 
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///pet_adoption_db'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_ECHO']= True
app.config['SQLALCHEMY_ECHO']= True if os.environ.get("TEST", "NOTTEST") == "NOTTEST" else False
app.config['SECRET_KEY']="oh-so-secret"
debug=DebugToolbarExtension(app)

connect_db(app)

@app.route("/base")
def show_base():
    """show base template page for reference"""
    return render_template("base.html")

@app.route("/pets")
def show_pets():
    """show all pets page shows all pets in our db!, renders a page with pets picture and avaialability. A pet's name can be clicked on to view the pets individual page."""
    all_pets=Pet.query.all()
    return render_template("petslist.html",pets=all_pets)

@app.route("/new", methods=["GET", "POST"])
def show_and_make_new_pet():
    """shows the new pet form and handles the form in a GET + POST route"""
    pet_form=AddPetForm()

    if pet_form.validate_on_submit():
        pet_name=pet_form.name.data
        pet_species=pet_form.species.data
        pet_image=pet_form.photo_url.data
        pet_age=pet_form.age.data
        pet_notes=pet_form.notes.data
        print(f"the new pet form data is name={pet_name}, species={pet_species}, age={pet_age}, notes={pet_notes}")
        new_pet=Pet(name=pet_name, species=pet_species, image_url=pet_image, age=pet_age, notes=pet_notes)
        db.session.add(new_pet)
        db.session.commit()
        flash("New pet created!!")
        flash(f"your new pet is {new_pet.name}, they are a {new_pet.species} with an id of {new_pet.id}", "success")
        return redirect("/pets")
    else:
        return render_template("addpetform.html", pet_form=pet_form)

@app.route("/<pet_id>", methods=["GET", "POST"])
def show_pet_details(pet_id):
    """show page for a pet's profile/ individual details alongside a form to edit a pet. Accepts GET and POST as a dual route."""
    integer_pet_id=int(pet_id)
    pet=Pet.query.get_or_404(integer_pet_id)
    pet_form=EditPetForm(obj=pet)

    if pet_form.validate_on_submit():
        pet_image=pet_form.photo_url.data
        pet_notes=pet_form.notes.data
        pet_available=pet_form.is_available.data
        print(f"the edit pet form data is photo url={pet_image}, avaiable={pet_available}, notes={pet_notes}")
        pet.image_url=pet_image
        pet.notes=pet_notes
        pet.available=pet_available
        db.session.commit()
        flash("Pet has been edited!!", "success")
        return redirect("/pets")
    else:
        return render_template("petdetail&edit.html", pet_form=pet_form, pet=pet)


@app.errorhandler(404)
def page_not_found(e):
    """Renders our custom 404 page if anything isn't found such as a missing pet"""
    return render_template('404.html', error=e), 404
