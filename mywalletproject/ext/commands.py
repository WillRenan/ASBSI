import click
from .database import db,User,Acoes,FundosImobiliarios

def create_db():
    """Creates database"""
    db.create_all()

def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_db():
    """Populate db with sample data"""
    data = [
        Acoes( name="Petro", condigo_acao="PETR4"),
        Acoes( name="Banco do Brasil", condigo_acao="BBAS3"),
        Acoes( name="Cemig", condigo_acao="CMIG4"),
    ]
    
    db.session.bulk_save_objects(data)
    db.session.commit()
    return Acoes.query.all()


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, populate_db]:
        app.cli.add_command(app.cli.command()(command))