from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    #add relationship in Messages model correct if needed
    messages = db.relationship('Message', backref='messenger', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_session_id = db.Column(db.String(30))
    question = db.Column(db.String(1500))
    bot_answer = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationship
    #user_id_relation = db.relationship("User")

    def __repr__(self):
        return 'Chat Session {}\nQuestion: {}\nAnswer: {}\nTimestamp: {}\n\n'.format(self.chat_session_id, self.question, self.bot_answer, self.timestamp)
