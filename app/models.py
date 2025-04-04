# app/models.py
from app.extensions import db

class Estudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(100))
    data = db.Column(db.String(10))  # ou db.Date
    categoria = db.Column(db.String(50))


