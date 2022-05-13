"""CRUD operations."""

from model import db, User, CampingSite, Rating, connect_to_db


#create a user with a password
def create_user(first_name,last_name, email, password):
    """Create and return a new user."""

    user = User(first_name=first_name, last_name=last_name, email=email, password=password)

    return user


if __name__ == '__main__':
    from server import app
    connect_to_db(app)