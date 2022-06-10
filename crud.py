"""CRUD operations."""

from model import db, User, CampingSite, Rating, connect_to_db


#create a user with a password
def create_user(first_name,last_name, email, password):
    """Create and return a new user."""

    user = User(
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        password=password)

    return user

def get_user_by_email(email):
    """Return a user by email."""
    print("*"*30)
    print(email)
    return User.query.filter(User.email == email).first()

def get_user_by_id(email):
    """Return a user's id."""

    
    return User.query.get(email).user_id()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)