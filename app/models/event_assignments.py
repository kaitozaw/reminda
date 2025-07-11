from app.extensions import db

class EventAssignment(db.Model):
    __tablename__ = "event_assignments"

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("google_events.id"), primary_key=True)
    assigned_at = db.Column(db.DateTime, server_default=db.func.now())

    customer = db.relationship("Customer", backref=db.backref("event_assignments", lazy=True))
    event = db.relationship("GoogleEvent", backref=db.backref("event_assignments", lazy=True))

    def __repr__(self):
        return f"<EventAssignment customer_id={self.customer_id} event_id={self.event_id}>"