from flask import  abort, render_template, redirect, Response, request, url_for
from ..ext.auth import login_required, logout_user, login_user, load_user,current_user
from curses import flash

from ..ext.database import User, Acoes,  FundosImobiliarios, db, check_password_hash

def init_app(app):
        
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
                abort(404)
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
    
    """ ------------------------------------------------- rotas dos templates-------------------------------------------- """
    @app.route('/login_temp', methods =['GET','POST'])
    def login_temp():
        print("www")
        if request.method == 'POST':

            email = request.form['email']
            senha = request.form['senha']
            user = User.query.filter_by(email=email).first()
            
            
            if user and check_password_hash(user.senha, senha):
                print("Senha correta!")
                login_user(user)
                return redirect(url_for('index'))
                
            else:
                abort(404)
                return redirect(url_for('login_temp'))

        return render_template('login_temp.html')
    
    @app.route('/cadastro_usuario_temp', methods =['GET','POST'])
    def cadastro_usuario_temp():
        if request.method == 'POST':
            
            usuario = User(request.form['nome'],request.form['email'],request.form['senha'])
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('login_temp'))
        
    

        return render_template('cadastro_usuario_temp.html')
    
    @app.route('/usuarios_tabelas_temp')
    def usuarios_tabelas_temp():
        usuarios = User.query.all()
        return render_template( 'usuarios_tabelas_temp.html',usuarios =usuarios)
    
    @app.route('/template_base')
    def template_base():
        return render_template('template_base.html')
    
    @app.route('/acoes', methods =['GET','POST'])
    @login_required
    def acoes():
        titulo = "Ações"
        if request.method == 'POST':
            #usuario = User.query.get(current_user.id)  # busca o usuário com id 
            acao = Acoes(request.form['nome_acao'], request.form['codigo_acao'],
                         usuario_id=current_user.id)


            #acao = Acoes(request.form['nome_acao'],request.form['codigo_acao'])
            db.session.add(acao)
            db.session.commit()
            return redirect(url_for('acoes'))
        
        usuario = current_user.id
        return render_template('acoes.html', titulo =titulo,usuario= usuario)

