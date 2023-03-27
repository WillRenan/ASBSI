from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import  SerializerMixin


""" bando de dados """
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flaskUser:@FlaskUser1234@localhost/developmentdb'

db = SQLAlchemy(app)

def init_app(app):
    db.init_app(app)

class Ativo(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(10))
    quant = db.Column(db.Integer)
    preco = db.Column(db.DNumeric())