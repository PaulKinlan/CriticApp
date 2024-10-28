import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

app = Flask(__name__)

# Configuration
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

# Database Configuration
if os.environ.get("DATABASE_URL"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    # Construct URL from individual components
    db_params = {
        'host': os.environ.get('PGHOST'),
        'port': os.environ.get('PGPORT'),
        'database': os.environ.get('PGDATABASE'),
        'user': os.environ.get('PGUSER'),
        'password': os.environ.get('PGPASSWORD')
    }
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize Flask-SQLAlchemy
db.init_app(app)

# Initialize Flask-Login
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

with app.app_context():
    from models import User, Critic, Document, Critique, CriticTemplate
    # Drop all tables and recreate them with new schema
    db.drop_all()
    db.create_all()
