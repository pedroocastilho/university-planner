from flask import Flask, render_template
import os
from app.extensions import db  # agora importa do extensions.py

def create_app():
    app = Flask(__name__)

    # 🔑 Define a chave secreta
    app.secret_key = 'uma-chave-secreta-segura'

    # Caminho do banco de dados
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, '..', 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importações dos blueprints
    from .modules.planner.routes import planner_bp
    from .modules.ocr.routes import ocr_bp
    from .modules.casos_clinicos.routes import casos_bp

    app.register_blueprint(planner_bp, url_prefix='/planner')
    app.register_blueprint(ocr_bp, url_prefix='/ocr')
    app.register_blueprint(casos_bp, url_prefix='/casos')

    # Página inicial
    @app.route('/')
    def home():
        return render_template('home.html')

    # Criar as tabelas no banco
    with app.app_context():
        db.create_all()

    return app
