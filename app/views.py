"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm
from models import UserProfile
import random

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        #if form.username.data:
            email = form.email.data
            password = form.password.data
            user = UserProfile.query.filter_by(email=email, password=password).first()
            if user is not None:
            
                login_user(user)
                flash('Logged in Successfully.', 'success')
                next = request.args.get('next')
            
                return redirect(url_for('secure_page'))
            else:
                flash('Username or Password is incorrect.', 'danger')
                return redirect(url_for('login'))
    return render_template("login.html", form=form)

#Creates user, saves to database
@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        userid = random.randint(2500, 30000)
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password  = form.password.data
    
        user = UserProfile(id=userid,
                           firstname=firstname,
                           lastname=lastname, 
                           email=email,
                           password=password)
        
        login_user(user)
        db.session.add(user)
        db.session.commit()

        flash('Profile for '+ firstname +' added','success')    
        return redirect(url_for('secure_page'))
    return render_template('register.html', form=form)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))
    
@app.route('/secure-page/')
@login_required
def secure_page():
    return render_template('secure-page.html')
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")