from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from db import DATABASE_URL
import os
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect

# Inicializaciones
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
csrf = CSRFProtect()

# Función principal
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Configuraciones comentadas (descomentar si son necesarias)
    app.secret_key = os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Clave secreta para firmar los JWTs
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 7200  # Expiración del token en segundos
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_CSRF_CHECK_FORM'] = True
    app.config['WTF_CSRF_ENABLED'] = True  # Si estás usando Flask-WTF
    app.config['JWT_CSRF_METHODS'] = ["POST", "PUT", "DELETE"]
    #Inicializar con la App
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    csrf.init_app(app) 
    
    #Registrar Blueprints

    from views.view import bp
    app.register_blueprint(bp)
    from views.auth import auth_bp
    app.register_blueprint(auth_bp)
    from views.user import user_bp
    app.register_blueprint(user_bp)

    #Manejo de errores    
    @app.errorhandler(401)
    def custom_401(error):
         return jsonify({"msg": "Token inválido o expirado"}), 401

    @app.errorhandler(422)
    def custom_422(error):
        return jsonify({"msg": "Token mal formado"}), 422

    return app
