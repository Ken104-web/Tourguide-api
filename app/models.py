from .extensions import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

class User(db.Model):
        __tablename__ = 'users'

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String, unique = True, nullable=False)
        email = db.Column(db.String, unique=True, nullable=False)
        password = db.Column(db.String)

        reviews = db.relationship('Review', backref='user')
        @validates('name')
        def  validates_name(self, key, name):
                if  not name:
                    raise ValueError('No name provided')
                return name
    
        @hybrid_property
        def password_hash(self):
            return self.password
        
        @password_hash.setter
        def password_hash(self, password):
            password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
            self.password = password_hash.decode('utf-8')
            
        def authenticate(self, password):
            return bcrypt.check_password_hash(self.password, password.encode('utf-8'))

class Site(db.Model):
        __tablename__ = 'sites'

        id = db.Column(db.Integer, primary_key=True)
        touristSite = db.Column(db.String)
        location = db.Column(db.String)
        description = db.Column(db.String)
        rating = db.Column(db.Integer)
        
        reviews = db.relationship('Review', backref='site')


class Review(db.Model):
    __tablename__ = "reviews"


    serialize_rules = ('-user.reviews','-site.reviews','-user.sites.reviews',)
    # serialize_rules = ('-users',)

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tourist_attraction_site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
