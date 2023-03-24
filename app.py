from flask import Flask, render_template, redirect, Response, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
Bootstrap(app)
app.config['TITLE'] = "MyWallet"

#-------------------------------DATABASE E TABELAS--------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mywallet.sqlite3'
db = SQLAlchemy(app)


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

class TipoAtivo(db.Model, SerializerMixin):
    __tablename__ = "tipoAtivo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, nome):
        self.nome = nome

class Acoes(db.Model, SerializerMixin):
    __tablename__ = "acoes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_acao = db.Column(db.String(80), unique=True, nullable=False)
    codigo_acao = db.Column(db.String(80), unique=True, nullable=False)
    
    def __init__(self, nome, codigo_acao):
        self.nome = nome
        self.codigo_acao = codigo_acao

class FundosImobiliarios(db.Model, SerializerMixin):
    __tablename__ = "fundosImobiliarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_fii = db.Column(db.String(80), unique=True, nullable=False)
    codigo_fii = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, nome,codigo_fii):
        self.nome = nome
        self.codigo_fii = codigo_fii


with app.app_context():
    db.create_all()
#-------------------------------ROTAS--------------------------------------------------
@app.route("/")
@app.route("/index")
def index():
    usuarios = User.query.all()
    return render_template("index.html", usuarios=usuarios)


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == 'POST':
        usuario = User(request.form['nome'],request.form['email'],request.form['senha'])
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete(id):
    usuario = User.query.get(id)
    print(usuario)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods =['GET','POST'])
def edit(id):
    usuario = User.query.get(id)
    if request.method == 'POST':
        print(usuario.nome)
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.senha = request.form['senha']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', usuario = usuario)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastrousuario', methods =['GET','POST'])
def cadastro():
    if request.method == 'POST':
        usuario = User(request.form['nome'],request.form['email'],request.form['senha'])
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('cadastrousuario.html')

if __name__ == '__main__':
  
    app.run(debug=True)
