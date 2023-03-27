from dynaconf import FlaskDynaconf
from curses import flash
from flask import Flask, render_template, redirect, Response, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


from flask_bootstrap import Bootstrap


from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
FlaskDynaconf(app)
Bootstrap(app)


#-------------------------------DATABASE E TABELAS--------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mywallet.sqlite3'
login_manager = LoginManager(app)
login_manager.init_app(app)
db = SQLAlchemy(app)


import os
app.secret_key = os.environ.get("FLASK_SECRET_KEY", default="um_segredo_muito_secreto")

#-------------------------------DATABASE E TABELAS--------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





#---------------------------------------------------------------------------------------------------
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

@app.route("/index")
@login_required
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
@app.route("/")
@app.route('/login', methods =['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        senha = request.form['senha']
        user = User.query.filter_by(email=email).first()
        

        if user and check_password_hash(user.senha, senha):
            print("Senha correta!")
            login_user(user)
            return redirect(url_for('index'))
            
        else:
            flash('Email ou senha inválidos.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/cadastrousuario', methods =['GET','POST'])
def cadastro():
    if request.method == 'POST':
        
        usuario = User(request.form['nome'],request.form['email'],request.form['senha'])
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('login'))
    


    return render_template('cadastrousuario.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
  
    app.run(debug=True)
