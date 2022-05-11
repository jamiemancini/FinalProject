"""Script to seed database."""

import os

import crud
import model
import server

os.system("dropdb wecamp")
os.system("createdb wecamp")

model.connect_to_db(server.app)
model.db.create_all()

