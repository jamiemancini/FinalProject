"""Models for Final Project NameTBD"""

from flask_sqalchemy import SQLAlchemy

db = SQAlchemy()

class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password=db.Column(db.String)
    
    def __repr__(self):
        # return f"<User user_id={self.user_id} first_name={self.first_name} last_name={self.last_name} email={self.email} password={sellf.passwprd}>"
        #not sure what to keep

class CampingSite(db.Model):
    """Campsites in CA State Parks and NPS"""

    __tablename__= "campsites"

    camping_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_name=db.Column(db.String)
    campsite_name=db.Column(db.String)
    park_type=db.Column(db.String)

    def __repr__(self):
        return f"<CampingSite camping_id={self.camping_id} "

class Rating(db.Model):
    """User Rating of Campsites"""

    __tablename__="ratings"

    user_id=