
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash,check_password_hash

#from flask_migrate import Migrate,MigrateCommand

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
 #   migrate = Migrate(app, db)
  #  app.cli.add_command('db', MigrateCommand)

class User(db.Model, SerializerMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)

    def verify_password(self, senha):
        return check_password_hash(self.senha, senha)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True


class TipoAtivo(db.Model, SerializerMixin):
    __tablename__ = "tipoAtivo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, nome):
        self.nome = nome

class Acoes(db.Model, SerializerMixin):
    __tablename__ = "acoes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    nome_acao = db.Column(db.String(80), nullable=False)
    codigo_acao = db.Column(db.String(80), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    data_compra = db.Column(db.String(10), nullable=False)
    
    def __init__(self, nome_acao, codigo_acao, usuario_id, quantidade, preco_unitario,data_compra):
        self.nome_acao = nome_acao
        self.codigo_acao = codigo_acao
        self.usuario_id = usuario_id
        self.quantidade  =  quantidade
        self.preco_unitario = preco_unitario
        self.data_compra =data_compra

class FundosImobiliarios(db.Model, SerializerMixin):
    __tablename__ = "fundosImobiliarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    nome_fii = db.Column(db.String(80), nullable=False)
    codigo_fii = db.Column(db.String(80), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    data_compra = db.Column(db.String(10), nullable=False)

    def __init__(self, nome,codigo_fii, usuario_id, quantidade, preco_unitario,data_compra):
        self.nome = nome
        self.codigo_fii = codigo_fii
        self.usuario_id = usuario_id
        self.quantidade  =  quantidade
        self.preco_unitario = preco_unitario
        self.data_compra =data_compra


