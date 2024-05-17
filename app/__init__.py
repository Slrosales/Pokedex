from flask import Flask
from flask_login import LoginManager

# Crear la instancia de la aplicación Flask
app = Flask(__name__)

# Configurar Flask-Login para manejo de sesiones
login_manager = LoginManager()
login_manager.init_app(app)

# Importar las rutas al final para evitar dependencias circulares
from app import routes
