from app.extensions import db

class GoogleEvent(db.Model):
    __tablename__ = "google_events"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    google_event_id = db.Column(db.String(128), nullable=False)
    calendar_id = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref=db.backref("events", lazy=True))

    def __repr__(self):
        return f"<GoogleEvent {self.title} ({self.start_time} - {self.end_time})>"