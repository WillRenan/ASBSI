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



    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login_temp'))
    
    """ ------------------------------------------------- rotas dos templates-------------------------------------------- """
    @app.route("/")
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
                return redirect(url_for('index_temp'))
                
            else:
                abort(404)
                return redirect(url_for('login_temp'))

        return render_template('login_temp.html')
    
    
    @app.route('/index_temp')
    def index_temp():
        return render_template('index_temp.html')
    
    @app.route('/cadastro_usuario_temp', methods =['GET','POST'])
    def cadastro_usuario_temp():
        if request.method == 'POST':
            
            usuario = User(request.form['nome'],request.form['email'],request.form['senha'])
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('login_temp'))
        
    

        return render_template('cadastro_usuario_temp.html')
    
    @app.route('/usuarios_tabelas_temp')
    @login_required
    def usuarios_tabelas_temp():
        usuarios = User.query.all()
        return render_template( 'usuarios_tabelas_temp.html',usuarios =usuarios)
    
    @app.route('/template_base')
    @login_required
    def template_base():
        return render_template('template_base.html')
    
    @app.route('/acoes', methods =['GET','POST'])
    @login_required
    def acoes():
        titulo = "Ações  "
        usuario = current_user.id

        if request.method == 'POST':
            acao = Acoes(nome_acao=request.form['nome_acao'], 
                         codigo_acao=request.form['codigo_acao'],
                         quantidade=request.form['quantidade'],
                         preco_unitario=request.form['preco_unitario'],
                         data_compra=request.form['data_compra'] ,   
                         usuario_id=current_user.id)

            #PERSISTENCIA NO BANCO DE DADOS
            db.session.add(acao)
            db.session.commit()
            return redirect(url_for('acoes'))
        
        acoes = Acoes.query.filter_by(usuario_id=current_user.id).all()
        
        return render_template('acoes.html', titulo =titulo,usuario= usuario,acoes=acoes)

    @app.route('/fundo_imobiliario', methods=['GET','POST'])
    @login_required
    def fundo_imobiliario():
        titulo = "Fundos Imobiliários"
        tituloSingular = "Fundo Imobiliário"
        usuario = current_user

        if request.method == 'POST':
            fundos = FundosImobiliarios(nome_fii=request.form['nome_fii'], 
                         codigo_fii=request.form['codigo_fii'],
                         quantidade=request.form['quantidade'],
                         preco_unitario=request.form['preco_unitario'],
                         data_compra=request.form['data_compra'] ,   
                         usuario_id=current_user.id)

            #PERSISTENCIA NO BANCO DE DADOS
            db.session.add(fundos)
            db.session.commit()
            return redirect(url_for('fundo_imobiliario'))
        
        fundosImobiliarios = FundosImobiliarios.query.filter_by(usuario_id=current_user.id).all()
        
        return render_template('fundo_imobiliario.html',
                               usuario=usuario, 
                               titulo=titulo,
                               tituloSingular=tituloSingular,
                               fundosImobiliarios=fundosImobiliarios)