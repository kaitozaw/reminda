from app.extensions import db
import enum

class ReminderStatus(enum.Enum):
    SENT = 'Sent'
    FAILED = 'Failed'

class ReminderLog(db.Model):
    __tablename__ = 'reminder_logs'

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('google_events.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sent_at = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.Enum(ReminderStatus), nullable=False)
    email_subject = db.Column(db.String(255))
    email_body = db.Column(db.Text)

    customer = db.relationship('Customer', backref=db.backref('reminder_logs', lazy=True))
    event = db.relationship('GoogleEvent', backref=db.backref('reminder_logs', lazy=True))
    user = db.relationship('User', backref=db.backref('reminder_logs', lazy=True))
    
    def __repr__(self):
        return f"<ReminderLog customer_id={self.customer_id} event_id={self.event_id} user_id={self.user_id} status={self.status.value}>"