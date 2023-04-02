from flask import  abort, render_template, redirect, Response, request, url_for,jsonify
from ..ext.auth import login_required, logout_user, login_user, load_user,current_user
from curses import flash

from ..ext.database import User, Acoes,  FundosImobiliarios, db, check_password_hash

def init_app(app):
        
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login_temp'))
    
    """ ------------------------------------------------- rotas dos templates-------------------------------------------- """
    @app.route("/")
    @app.route('/login_temp', methods =['GET','POST'])
    def login_temp():
        #print("www")
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
                return redirect(url_for('erro_404'))

        return render_template('login_temp.html')
    
    @app.route('/404')
    def erro_404():
        return render_template('404.html')
    
    @app.route('/index_temp')
    def index_temp():
        fundosImobiliarios = FundosImobiliarios.query.filter_by(usuario_id=current_user.id).all()
        acoes = Acoes.query.filter_by(usuario_id=current_user.id).all()
        usuario =current_user

        data = {
             'fundosImobiliarios': [f.to_dict() for f in fundosImobiliarios],
             'acoes': [a.to_dict() for a in acoes]
        }

        total_acoes = 0.0
        total_quant_acoes = 0 
        for acao in acoes:
           total_acoes += acao.quantidade * acao.preco_unitario
           total_quant_acoes += acao.quantidade

        total_fundos = 0.0
        total_quant_fundos =0
        for fundo in fundosImobiliarios:
           total_fundos += fundo.quantidade * fundo.preco_unitario
           total_quant_fundos += fundo.quantidade
        

        total_acoes = round(total_acoes, 2)
        total_acoes = str(total_acoes).replace('.', ',')

        total_fundos = round(total_fundos, 2)
        total_fundos = str(total_fundos).replace('.', ',')


        return render_template('index_temp.html',
                                acoes=acoes,
                                fundosImobiliarios=fundosImobiliarios,
                                usuario=usuario,
                                total_acoes=total_acoes,
                                total_fundos=total_fundos,
                                total_quant_acoes=total_quant_acoes,
                                total_quant_fundos =total_quant_fundos )  
    







    
    
    
    @app.route('/cadastro_usuario_temp', methods =['GET','POST'])
    def cadastro_usuario_temp():
        if request.method == 'POST':
            
            usuario = User(request.form['nome'],request.form['email'],request.form['senha'])
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('login_temp'))
        
    

        return render_template('cadastro_usuario_temp.html')
    
    @app.route('/usuarios_tabelas_temp', methods =['GET','POST'])
    @login_required
    def usuarios_tabelas_temp():
        usuarios = User.query.all()
        fundosImobiliarios = FundosImobiliarios.query.all()
        acoes = Acoes.query.all()

        return render_template( 'usuarios_tabelas_temp.html',
                               usuarios =usuarios,
                               fundosImobiliarios=fundosImobiliarios,
                               acoes=acoes)
    
    @app.route('/template_base')
    @login_required
    def template_base():
        return render_template('template_base.html')
    
    @app.route('/acoes', methods =['GET','POST'])
    @login_required
    def acoes():
        titulo = "Ações"
        tituloSingular = "Ação"
        usuario = current_user

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
        
        return render_template('acoes.html', 
                               titulo =titulo,
                               usuario= usuario,
                               acoes=acoes,
                               tituloSingular=tituloSingular)

    @app.route('/fundo_imobiliario', methods=['GET','POST'])
    @login_required
    def fundo_imobiliario():
        titulo = "Fundos Imobiliários"
        tituloSingular = "Fundo Imobiliário"
        usuario = current_user

        if request.method == 'POST':
            fundos = FundosImobiliarios(
                         nome_fii=request.form['nome_fii'], 
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
    


    # edidar
    
    @app.route('/edit_fundo/<int:id>', methods =['GET','POST'])
    def edit_fundo(id):
        fundo= FundosImobiliarios.query.get(id)
        if request.method == 'POST':

            fundo.nome_fii=request.form['nome_fii'], 
            fundo.codigo_fii=request.form['codigo_fii'],
            fundo.quantidade=request.form['quantidade'],
            fundo.preco_unitario=request.form['preco_unitario'],
            fundo.data_compra=request.form['data_compra'] 

            db.session.commit()
            return redirect(url_for('fundo_imobiliario'))
        usuario = current_user
        return render_template('editar_fundos.html', fundo = fundo)
    

    #deletar
    @app.route('/delete/<tipo>/<int:id>')
    def delete(tipo,id):
        
        if tipo == 'fundos':
            fundo = FundosImobiliarios.query.get(id)
            db.session.delete(fundo)
        elif tipo == 'acao':
            acao = Acoes.query.get(id)
            db.session.delete(acao)

        
        db.session.commit()
        return redirect(url_for('fundo_imobiliario'))