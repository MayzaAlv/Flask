import mimetypes
from flask import Blueprint, redirect, render_template, request, flash, url_for, Response
from flask_login import login_required, current_user
from .models import Petcard
from . import db
from datetime import date, datetime

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    petcard = Petcard.query.filter_by(owner=current_user.id).all()
    return render_template('home.html', user=current_user, petcard=petcard)


@views.route("/register", methods=["GET", "POST"])
@login_required
def register():
    format = "%Y-%m-%d"
    
    if request.method == "POST":
        name = request.form.get("name").title()
        image = request.files["image"]
        birthday = request.form.get("birthday")
        birthday = datetime.strptime(birthday, format).date()
        breed = request.form.get("breed")
        gender = request.form.get("gender")
        mimetype = image.mimetype
        
        if not name:
            flash("Name cannot be empty", category="error")
        elif not birthday:
            flash("Birthday cannot be empty", category="error")
        elif not breed:
            flash("Breed cannot be empty", category="error")
        elif not gender:
            flash("Gender cannot be empty", category="error")
        elif not image:
            flash("Image cannot be empty", category="error")
        
        else:
            petcard = Petcard(name=name, image=image.read(), birthday=birthday, breed=breed, 
                              gender=gender, owner=current_user.id, mimetype=mimetype)
            db.session.add(petcard)
            db.session.commit()
            flash("Petcard created!", category="sucess")
            return redirect(url_for("views.home"))
            
    return render_template('registerPet.html', user=current_user)


@views.route("/petcard/<int:id>/image")
def render_image(id):
    petcard = Petcard.query.filter_by(id=id).first()
    if not petcard:
        return 'No img with that id', 404
    return Response(petcard.image, mimetype=petcard.mimetype)


@views.route("/petcard/<int:id>/delete")
def delete_petcard(id):
    petcard = Petcard.query.filter_by(id=id).first()
    db.session.delete(petcard)
    db.session.commit()
    
    return redirect(url_for("views.home"))


@views.route("/petcard/<int:id>/edit",  methods=["GET", "POST"])
def edit_petcard(id):
    petcard = Petcard.query.filter_by(id=id).first()
    
    if request.method == "POST":
        format = "%Y-%m-%d"
        
        petcard.name = request.form.get("name").title()
        birthday = request.form.get("birthday")
        birthday = datetime.strptime(birthday, format).date()
        petcard.breed = request.form.get("breed")
        petcard.gender = request.form.get("gender")
        if request.files["image"]:
            petcard.image = request.files["image"].read()
            petcard.mimetype = request.files["image"].mimetype
        
        db.session.add(petcard)
        db.session.commit()
        return redirect(url_for("views.home"))
    
    return render_template('registerPet.html', user=current_user, petcard=petcard)
