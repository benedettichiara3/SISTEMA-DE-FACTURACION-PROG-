import os

class Config:
    SECRET_KEY = "clave_secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///facturacion.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
