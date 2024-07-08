import os

class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.getenv("DATAB")