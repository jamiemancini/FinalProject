"""CRUD operations."""

from model import db, User, Rating, connect_to_db


def create_user(first_name,last_name, email, password):
    """Create and return a new user."""

    user = User(
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        password_hash=password)

    return user

def get_user_by_email(email):
    """Return a user by email."""
    
    return User.query.filter(User.email == email).first()

def get_user_by_id(user_id):
    """Return a user by id."""
    
    return User.query.get(user_id)

def create_rating(user_id, camp_name, camping_id, review_description, review_score):
    """Creates a Rating"""
    rating = Rating(
            user_id=user_id,
            camp_name=camp_name,
            camping_id=camping_id,
            review_description=review_description,
            review_score=review_score)
    return rating

def get_rating_by_user_id(user_id):
    """Returns the ratings by user_id"""

    return Rating.query.filter(Rating.user_id==user_id).all()

def get_rating_by_camping_id(camping_id):
    """Returns the ratings by camping_id"""

    return Rating.query.filter(Rating.camping_id==camping_id).all()

# def create_note(user_id, camping_id, camping_name, activity_notes, campsite_notes, park_notes):
#     """Creates a Note"""
#     note = Note(
#             user_id=user_id,
#             camping_id=camping_id,
#             camping_name=camping_name,
#             activity_notes=activity_notes,
#             campsite_notes=campsite_notes,
#             park_notes=park_notes)

#     return note

# def get_notes_by_user_id(user_id):
#     """Returns the notes by user_id"""

#     return Note.query.filter(Note.user_id==user_id).all()

# def get_notes_by_camping_id(camping_id):
#     """Returns the notes by user_id"""

#     return Note.query.filter(Note.camping_id==camping_id).all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)