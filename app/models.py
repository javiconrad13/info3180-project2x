from . import db

class UserProfile(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    items = db.relationship('Wish', backref="users")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
        
class Wish(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    thumbnail = db.Column(db.String(225))
    title = db.Column(db.String(80))
    description = db.Column(db.String(255))
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Wish %r>' % (self.title)
