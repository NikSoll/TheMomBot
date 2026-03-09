import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'simple-dev-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bots.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_DIR = 'bots'
    BOTS_DIR = 'bots'