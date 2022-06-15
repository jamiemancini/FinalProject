"""Models for Final Project WECamp"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(UserMixin, db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                            autoincrement=True, 
                            primary_key=True,
                            unique=True)

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120),
                            unique=True)
    password_hash=db.Column(db.String(130))
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return self.password_hash == password
        # return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User user_id={self.user_id} first_name={self.first_name} last_name={self.last_name}>"


class CampingSite(db.Model):
    """Campsites in CA State Parks and NPS"""

    __tablename__= "campsites"

    camping_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    park_name=db.Column(db.String)
    campsite_name=db.Column(db.String)
    park_type=db.Column(db.String)

    def __repr__(self):
        return f"<CampingSite camping_id={self.camping_id}  park_name={self.park_name}>"

class Rating(db.Model):
    """User Rating of Campsites"""

    __tablename__="ratings"

    rating_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey("users.user_id"))
    camping_id=db.Column(db.Integer, db.ForeignKey("campsites.camping_id"))
    review_description=db.Column(db.Text)
    review_score=db.Column(db.Integer)

    campsite = db.relationship("CampingSite", backref="ratings")
    user = db.relationship("User", backref="ratings")

    def __repr__(self):
        return f"<Rating user_id={self.user_id} camping_id{self.camping_id}> "

def connect_to_db(flask_app, db_uri="postgresql:///wecamp", echo=True):
    """connect to database"""

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app) #do I need to add the name of the tables afterwards?
    
