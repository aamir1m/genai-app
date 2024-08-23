from flask import Flask
from flask_cors import CORS
from config import Config

def create_app(config_class=Config):
    # Create the Flask app instance
    app = Flask(__name__)
    
    # Apply configuration settings
    app.config.from_object(config_class)
    
    CORS(app)  # Enable CORS

    # Import routes to register them with the app
    with app.app_context():
        from app.routes import hello

    return app
