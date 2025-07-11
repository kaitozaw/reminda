from app.extensions import db
from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    reminder_offset = db.Column(db.Integer, default=0)
    reminder_hour = db.Column(db.Integer, default=9)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (
        CheckConstraint('reminder_offset IN (0, 1)', name='check_reminder_offset'),
        CheckConstraint('reminder_hour BETWEEN 0 AND 23', name='check_reminder_hour'),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.id} {self.email}>"