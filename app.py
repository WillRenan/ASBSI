from flask import Flask, render_template, redirect, Response, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
Bootstrap(app)
app.config['TITLE'] = "MyWallet"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudantes.sqlite3'
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

with app.app_context():
    db.create_all()

@app.route("/")
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


if __name__ == '__main__':
  
    app.run(debug=True)
