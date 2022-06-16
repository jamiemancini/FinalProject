"""CRUD operations."""

from model import db, User, Rating, connect_to_db


#create a user with a password
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
    print("*"*30)
    print(email)
    return User.query.filter(User.email == email).first()

def get_user_by_id(user_id):
    """Return a user by id."""
    return User.query.get(user_id)

def create_rating(user_id, camping_id,review_description, review_score):
    """Creates a Rating"""
    rating = Rating(
            user_id=user_id,
            camping_id=camping_id,
            review_description=review_description,
            review_score=review_score)
    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)