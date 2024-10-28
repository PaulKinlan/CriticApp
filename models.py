from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships
    documents = db.relationship('Document', backref='user', lazy=True)
    critics = db.relationship('Critic', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Critic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    persona = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    critique_mode = db.Column(db.String(20), nullable=False, default='detailed')  # 'quick' or 'detailed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    critiques = db.relationship('Critique', backref='document', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Critique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    critic_id = db.Column(db.Integer, db.ForeignKey('critic.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    critic = db.relationship('Critic', backref='critiques')

class CriticTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    persona = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., 'academic', 'technical', 'content'
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
