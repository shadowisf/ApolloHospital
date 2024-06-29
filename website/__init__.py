from flask import Flask
from flask_compress import Compress

compress = Compress()

def create_app():
    app = Flask(__name__)
    compress.init_app(app)
    app.config['SECRET_KEY'] = "posjfsojfsdojfpsjfopsj"
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    return app