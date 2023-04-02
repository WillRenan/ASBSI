from flask import Flask

from mywalletproject.ext import configuration

def create_app():
    app = Flask(__name__)
    configuration.init_app(app)
    configuration.load_extensions(app)
    return app


import os
app = create_app()
app.secret_key = os.environ.get("FLASK_SECRET_KEY", default="um_segredo_muito_secreto")
""" if __name__ == '__main__':
  
    app.run(debug=True)
 """