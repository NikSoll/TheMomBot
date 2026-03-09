import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = 'dev-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bots.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOTS_DIR = 'bots/generated'
    TEMPLATES_DIR = 'bots/tg'