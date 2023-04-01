from flask import Flask

from mywalletproject.ext import configuration
from mywalletproject.ext import database

from mywalletproject.ext import auth
from mywalletproject.ext import bootstrap
from mywalletproject.ext import commands

#from flask_migrate import MigrateCommand

#BLUEPRINTS 
from mywalletproject.blueprints import views
from mywalletproject.blueprints import restapi

app = Flask(__name__)





configuration.init_app(app)
database.init_app(app)
auth.init_app(app)
views.init_app(app)
bootstrap.init_app(app)
restapi.init_app(app)
commands.init_app(app)



import os
app.secret_key = os.environ.get("FLASK_SECRET_KEY", default="um_segredo_muito_secreto")
if __name__ == '__main__':
  
    app.run(debug=True)
