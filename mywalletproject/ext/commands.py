from ctypes import create_string_buffer
import click
from .database import db,User,Acoes,FundosImobiliarios
from werkzeug.security import generate_password_hash

def create_db():
    """Creates database"""
    db.create_all()

def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_db():
    """Populate db with sample data"""
    users = [
        User(nome="João", email="joao@example.com", senha=generate_password_hash("123")),
        User(nome="Maria", email="maria@example.com", senha=generate_password_hash("123")),
        User(nome="Pedro", email="pedro@example.com", senha=generate_password_hash("123")),
    ]

    db.session.bulk_save_objects(users)

    db.session.commit()

    return User.query.all()


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, populate_db]:
        app.cli.add_command(app.cli.command()(command))

    # add a single command
    @app.cli.command()
    @click.option('--username', '-u')
    @click.option('--password', '-p')
    def add_user(username, password):
        """Adds a new user to the database"""
        return create_string_buffer(username, password)