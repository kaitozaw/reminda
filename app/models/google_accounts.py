from app.extensions import db

class GoogleAccount(db.Model):
    __tablename__ = 'google_accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    google_id = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(512), nullable=True)
    refresh_token = db.Column(db.String(512), nullable=True)
    token_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref=db.backref("google_account", uselist=False, lazy=True))

    def __repr__(self):
        return f"<GoogleAccount user_id={self.user_id} email={self.email}>"