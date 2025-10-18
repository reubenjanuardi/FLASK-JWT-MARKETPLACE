from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import ekstensi dan blueprint
from extensions import jwt
from config.database import init_db 
from routes.auth_routes import auth_bp, register_jwt_callbacks
from routes.item_routes import item_bp
from models.user import User
from models.item import Item

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Inisialisasi database
init_db(app)

# Konfigurasi JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 900  # Setting token expired 15 menit
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 604800  # 7 hari (dalam detik)

# Inisialisasi ekstensi
jwt.init_app(app)
register_jwt_callbacks(jwt)

# Register blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(item_bp, url_prefix='/items')

# Default route
@app.route('/')
def home():
    return {"message": "Welcome to JWT Marketplace API"}

if __name__ == "__main__":
    app.run(debug=True)
