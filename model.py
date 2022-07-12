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

class Rating(db.Model):
    """User Rating of Campsites"""

    __tablename__="ratings"

    rating_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey("users.user_id"))
    camp_name=db.Column(db.Text)
    camping_id=db.Column(db.String)
    review_description=db.Column(db.Text)
    review_score=db.Column(db.Integer)

    user = db.relationship("User", backref="ratings")
    
    def __repr__(self):
        return f"<Rating user_id={self.user_id} camping_id={self.camping_id} review: {self.review_description} score: {self.review_score}> "

# class Note(db.Model):
#     """User Notes of Campsites"""

#     __tablename__="notes"

#     note_id=db.Column(db.Integer,autoincrement=True,primary_key=True, unique=True)
#     user_id= db.Column(db.Integer, db.ForeignKey("users.user_id"))
#     camping_id=db.Column(db.String)
#     camping_name=db.Column(db.String)
#     activity_notes=db.Column(db.Text)
#     campsite_notes=db.Column(db.Text)
#     park_notes= db.Column(db.Text)

#     user = db.relationship("User", backref="notes")


    # def __repr__(self):
    #     return f"<Note note_id ={self.note_id} user_id={self.user_id} camping_id={self.camping_id}> "        

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

    

    connect_to_db(app) 
    
