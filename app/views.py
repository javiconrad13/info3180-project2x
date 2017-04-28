"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm, WishForm
from models import UserProfile, Wish
import random
import requests
import BeautifulSoup
import urlparse

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
    
@app.route("/api/users/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))

###
#Wishlist
###
@app.route("/api/users/<userid>/wishlist", methods=["GET","POST"])
def wishlist(userid): 
    form = WishForm()
    form2= LoginForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            user = db.session.query(UserProfile).filter_by(id=userid).first()
            url = form.url.data
            thumbnail = form.thumbnail.data
            title = form.thumbnail.data
            description = form.description.data
            
            wish = Wish(url = url,
                            thumbnail = thumbnail,
                            title = title,
                            description = description,
                            userid = user.id)
    
            if wish:
                db.session.add(wish)
                db.session.commit()
                flash(''+title+' was added to your wishlist', 'success')
                response = jsonify({"error":"null",
                                    "data":{'userid':userid,
                                            'url':url,
                                            'thumbnail':thumbnail,
                                            'title':title,
                                            'description':description},
                                    "message":"Success"})
                return redirect(url_for('wishlist', userid=user.id))
            else:
                response = jsonify({"error":"1", 
                                    "data":{}, 
                                    "message":"Wish not created"})
                flash('Invalid item data, please try again', 'danger')
            return redirect(url_for('wishlist', userid=user.id))
    else:
        user = db.session.query(UserProfile).filter_by(id=userid).first()
        wishes = db.session.query(Wish).filter_by(userid=user.id).all()
        wishlist = []
        
        for wish in wishes:
            wishlist.append({'title':wish.title,'url':wish.url,'thumbnail':wish.thumbnail,'description':wish.description})
        if(len(wishlist)>0):
            response = jsonify({"error":"null","data":{"user":user.firstname + " " + user.lastname, "wishes":wishlist},"message":"Success"})
        else:
            response = jsonify({"error":"1","data":{},"message":"Unable to get wishes"})
    return render_template('wishlist.html', wishes=wishes, userid=userid, form=form, form2=form2)

#NEEDS WORK - Avoiding for now
@app.route('/api/users/<userid>/wishlist/<itemid>', methods=["DELETE"])
def removeWish(userid, itemid):
    user = db.session.query(UserProfile).filter_by(id=userid).first()
    if not user:
        response = jsonify({'message':'User not found'})
        response.status_code = 404
        return response
    itemlist = map(lambda x: x.id , user.items)
    if not int(itemid) in itemlist:
        response = jsonify({'message': 'No such item'})
        response.status_code = 404
        return response
    db.session.query(Wish).filter_by(id=itemid).delete()
    db.session.commit()
    response = jsonify({})
    response.status_code = 204
    return response
    
###
# The functions below should be applicable to all Flask apps.
###
@app.route('/api/thumbnails/', methods=["GET"])
def imgs():
    #url = "http://s5.photobucket.com/"
    url = request.args.get('url')
    soup = BeautifulSoup.BeautifulSoup(requests.get(url).text)
    images = BeautifulSoup.BeautifulSoup(requests.get(url).text).findAll("img")
    imagelist = []    
    
    og_image = (soup.find('meta', property='og:image') or soup.find('meta', attrs={'name': 'og:image'}))
                        
    if og_image and og_image['content']:
        imagelist.append(urlparse.urljoin(url, og_image['content']))
    
    thumbnail_spec = soup.find('link', rel='image_src')
    if thumbnail_spec and thumbnail_spec['href']:
        imagelist.append(urlparse.urljoin(url, thumbnail_spec['href']))
    
    for img in images:
        if "sprite" not in img["src"]:
            imagelist.append(urlparse.urljoin(url, img['src']))

    if(len(imagelist)>0):
        response = jsonify({'error':'null', "data":{"thumbnails":imagelist},"message":"Success"})
    else:
        response = jsonify({'error':'1','data':{},'message':'Unable to extract thumbnails'})
    return response


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