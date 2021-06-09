from os import environ
from app import create_app
environ["APP_ENV"] = "Prod"
application = create_app()