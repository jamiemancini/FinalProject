"""Models for Final Project WECamp"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password=db.Column(db.String)
    
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

    connect_to_db(app)
