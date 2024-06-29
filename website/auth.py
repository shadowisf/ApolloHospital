#import requirments
from flask import Blueprint, render_template,request, flash,redirect,url_for
from .auth_utils import *
from .views import *

# url routing for all authentication and registration
auth = Blueprint("auth", __name__)



@auth.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        if user_type == 'receptionist':
            if authenticate_receptionist(username, password):
                flash(f"login successful! welcome, receptionist {username}!")
                return redirect(url_for("views.reception"))
        elif user_type == 'doctor':
            if authenticate_doctor(username, password):
                flash(f"login successful! welcome, doctor {username}!")
                return redirect(url_for("views.doctor_app"))
        elif user_type == 'staff':
            if authenticate_staff(username, password):
                flash(f"login successful! welcome, staff {username}!")
                return redirect(url_for("views.staff"))
        flash(f"incorrect login credentials! please try again.")
    return render_template("general_webpages/login.html")


#redirect page back home
@auth.route("/sign-up", methods = ['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        if user_type == 'receptionist':
            if register_receptionist(username, email, password):
                flash("receptionist registered successfully!")
                return render_template("general_webpages/sign_up.html")
        elif user_type == 'doctor':
            if register_doctor(username, email, password):
                flash("doctor registered successfully!")
                return render_template("general_webpages/sign_up.html")
        elif user_type == 'staff':
            if register_staff(username, email, password):
                flash("staff registered successfully!")
                return render_template("general_webpages/sign_up.html")
        # return redirect(url_for("views.signUpError"))
        flash(f"credentials already taken or invalid! please try again.")
    return render_template("general_webpages/sign_up.html")


@auth.route("/logout")
def logout():
    return redirect(url_for('views.home'))