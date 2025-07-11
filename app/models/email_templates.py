from app.extensions import db

class EmailTemplate(db.Model):
    __tablename__ = "email_templates"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    template_subject = db.Column(db.String(255), nullable=False)
    template_body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref=db.backref("email_template", uselist=False, lazy=True))

    def __repr__(self):
        return f"<EmailTemplate {self.id} user={self.user_id}>"