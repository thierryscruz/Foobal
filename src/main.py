import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.futebol import SessaoFutebol
from src.routes.user import user_bp
from src.routes.futebol import futebol_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações para produção e desenvolvimento
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Configurar CORS para permitir requisições do frontend
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(futebol_bp, url_prefix='/api/futebol')

# Configuração do banco de dados
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Para PostgreSQL no Render
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(f"Usando PostgreSQL: {database_url[:50]}...")
else:
    # Para desenvolvimento local
    sqlite_path = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_path
    print(f"Usando SQLite: {sqlite_path}")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
db.init_app(app)

with app.app_context():
    # Criar diretório do banco se não existir (apenas para SQLite local)
    if not database_url:
        os.makedirs(os.path.join(os.path.dirname(__file__), 'database'), exist_ok=True)
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)

