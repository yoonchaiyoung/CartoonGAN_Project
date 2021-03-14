from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager
)
import ssl

def create_app():
    app = Flask(__name__)
    app.config.update(SECRET_KEY="bit-cartoon")
    jwt = JWTManager(app)

    from model import account, cartoon, gallery

    app.register_blueprint(account.bp_login)
    app.register_blueprint(cartoon.bp_cartoon)
    app.register_blueprint(gallery.bp_gallery)

    return app

if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='./ssl/server.crt', keyfile='./ssl/server.key', password='jong!6763')
    app = create_app()
    CORS(app)
    # app.run("0.0.0.0", port=5000, debug=True)
    app.run("0.0.0.0", port=5000, debug=True, ssl_context=ssl_context)