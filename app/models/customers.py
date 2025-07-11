from app.extensions import db

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    tel = db.Column(db.String(20))
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref=db.backref("customers", lazy=True))

    def __repr__(self):
        return f"<Customer {self.id} {self.first_name} {self.last_name}>"