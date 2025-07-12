from app.extensions import csrf, db
from app.models import Customer, EventAssignment, GoogleAccount,  GoogleEvent, User
from app.utils.google_api import fetch_google_event_data
from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy import or_

bp = Blueprint("addon", __name__)

def get_user_id_from_email(email):
    ga = GoogleAccount.query.filter_by(email=email).first()
    return ga.user_id if ga else None

@bp.route("/api/customers", methods=["GET"])
def get_customers():
    email = request.args.get("user_email")
    query = request.args.get("query", "").strip()
    user_id = get_user_id_from_email(email)
    if not user_id:
        return jsonify({"error": "User not found"}), 404

    customers = Customer.query.filter(
        Customer.user_id == user_id,
        or_(
            Customer.first_name.ilike(f"%{query}%"),
            Customer.last_name.ilike(f"%{query}%"),
            Customer.location.ilike(f"%{query}%")
        )
    ).all()

    return jsonify([{
        "id": c.id,
        "first_name": c.first_name,
        "last_name": c.last_name,
        "location": c.location
    } for c in customers]), 200

@bp.route("/api/customers", methods=["POST"])
@csrf.exempt
def create_customer():
    email = request.args.get("user_email")
    user_id = get_user_id_from_email(email)
    if not user_id:
        return jsonify({"error": "User not found"}), 404

    data = request.json

    customer = Customer(
        user_id=user_id,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        tel=data.get("tel"),
        location=data.get("location"),
        description=data.get("description")
    )
    db.session.add(customer)
    db.session.commit()

    return jsonify({"message": "Customer created", "id": customer.id}), 201

@bp.route("/api/customers/<int:customer_id>", methods=["GET"])
def get_customer_detail(customer_id):
    email = request.args.get("user_email")
    user_id = get_user_id_from_email(email)
    if not user_id:
        return jsonify({"error": "User not found"}), 404

    customer = Customer.query.filter_by(id=customer_id, user_id=user_id).first_or_404()
    now = datetime.utcnow()

    events = (
        db.session.query(GoogleEvent)
        .join(EventAssignment)
        .filter(
            EventAssignment.customer_id == customer_id,
            GoogleEvent.start_time >= now
        )
        .order_by(GoogleEvent.start_time.asc())
        .all()
    )
    
    return jsonify({
        "id": customer.id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "tel": customer.tel,
        "location": customer.location,
        "description": customer.description,
        "upcoming_events": [{
            "title": e.title,
            "start_time": e.start_time.isoformat()
        } for e in events]
    }), 200

@bp.route("/api/customers/<int:customer_id>", methods=["PUT"])
@csrf.exempt
def update_customer(customer_id):
    email = request.args.get("user_email")
    user_id = get_user_id_from_email(email)
    if not user_id:
        return jsonify({"error": "User not found"}), 404

    customer = Customer.query.filter_by(id=customer_id, user_id=user_id).first_or_404()
    data = request.json

    customer.first_name = data.get("first_name", customer.first_name)
    customer.last_name = data.get("last_name", customer.last_name)
    customer.email = data.get("email", customer.email)
    customer.tel = data.get("tel", customer.tel)
    customer.location = data.get("location", customer.location)
    customer.description = data.get("description", customer.description)
    db.session.commit()

    return jsonify({"message": "Customer updated", "id": customer.id}), 200

@bp.route("/api/customers/<int:customer_id>", methods=["DELETE"])
@csrf.exempt
def delete_customer(customer_id):
    email = request.args.get("user_email")
    user_id = get_user_id_from_email(email)
    if not user_id:
        return jsonify({"error": "User not found"}), 404

    customer = Customer.query.filter_by(id=customer_id, user_id=user_id).first_or_404()

    assignments = EventAssignment.query.filter_by(customer_id=customer.id).all()
    for assignment in assignments:
        event_id = assignment.event_id
        db.session.delete(assignment)

        remaining = EventAssignment.query.filter_by(event_id=event_id).count()
        if remaining == 0:
            google_event = GoogleEvent.query.get(event_id)
            if google_event:
                db.session.delete(google_event)

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted"}), 200

@bp.route("/api/events/is_assigned", methods=["GET"])
def is_event_assigned():
    email = request.args.get("user_email")
    google_event_id = request.args.get("google_event_id")
    user_id = get_user_id_from_email(email)
    if not user_id:
        return jsonify({"assigned": False}), 404
    
    google_event = GoogleEvent.query.filter_by(user_id=user_id, google_event_id=google_event_id).first()
    if not google_event:
        return jsonify({"assigned": False})

    exists = db.session.query(db.session.query(EventAssignment).filter_by(event_id=google_event.id).exists()).scalar()

    return jsonify({"assigned": exists}), 200

@bp.route("/api/events/is_assigned_to_customer", methods=["GET"])
def is_assigned_to_customer():
    email = request.args.get("user_email")
    google_event_id = request.args.get("google_event_id")
    customer_id = request.args.get("customer_id")
    user_id = get_user_id_from_email(email)
    if not user_id or not google_event_id or not customer_id:
        return jsonify({"assigned": False}), 400

    google_event = GoogleEvent.query.filter_by(user_id=user_id, google_event_id=google_event_id).first()
    if not google_event:
        return jsonify({"assigned": False}), 200
    

    assignment_exists = EventAssignment.query.filter_by(event_id=google_event.id, customer_id=customer_id).first() is not None
    
    return jsonify({"assigned": assignment_exists}), 200

@bp.route("/api/events/assigned", methods=["GET"])
def get_assigned_customers():
    email = request.args.get("user_email")
    google_event_id = request.args.get("google_event_id")
    query = request.args.get("query", "").strip()
    user_id = get_user_id_from_email(email)
    if not user_id:
        return jsonify({"error": "User not found"}), 404

    google_event = GoogleEvent.query.filter_by(user_id=user_id, google_event_id=google_event_id).first_or_404()

    assigned_subquery = (EventAssignment.query.with_entities(EventAssignment.customer_id).filter_by(event_id=google_event.id).subquery())

    filters = [Customer.user_id == user_id, Customer.id.in_(assigned_subquery)]
    if query:
        filters.append(
            or_(
                Customer.first_name.ilike(f"%{query}%"),
                Customer.last_name.ilike(f"%{query}%"),
                Customer.location.ilike(f"%{query}%")
            )
        )
    
    customers = Customer.query.filter(*filters).all()

    return jsonify([{
        "id": c.id,
        "first_name": c.first_name,
        "last_name": c.last_name,
        "location": c.location
    } for c in customers]), 200

@bp.route("/api/events/available", methods=["GET"])
def get_available_customers():
    email = request.args.get("user_email")
    google_event_id = request.args.get("google_event_id")
    query = request.args.get("query", "").strip()
    user_id = get_user_id_from_email(email)
    if not user_id:
        return jsonify({"error": "User not found"}), 404
    
    google_event = GoogleEvent.query.filter_by(user_id=user_id, google_event_id=google_event_id).first_or_404()

    assigned_subquery = (EventAssignment.query.with_entities(EventAssignment.customer_id).filter_by(event_id=google_event.id).subquery())

    filters = [Customer.user_id == user_id, ~Customer.id.in_(assigned_subquery)]
    if query:
        filters.append(
            or_(
                Customer.first_name.ilike(f"%{query}%"),
                Customer.last_name.ilike(f"%{query}%"),
                Customer.location.ilike(f"%{query}%")
            )
        )
    customers = Customer.query.filter(*filters).all()

    return jsonify([{
        "id": c.id,
        "first_name": c.first_name,
        "last_name": c.last_name,
        "location": c.location
    } for c in customers]), 200

@bp.route("/api/events/assign", methods=["POST"])
@csrf.exempt
def assign_customer():
    email = request.args.get("user_email")
    google_event_id = request.args.get("google_event_id")
    user_id = get_user_id_from_email(email)
    if not user_id:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    customer_id = data.get("customer_id")
    calendar_id = data.get("calendar_id")

    customer = Customer.query.filter_by(id=customer_id, user_id=user_id).first_or_404()

    google_event = GoogleEvent.query.filter_by(user_id=user_id, google_event_id=google_event_id).first()
    if not google_event:
        google_account = GoogleAccount.query.filter_by(user_id=user_id).first()
        if not google_account:
            return jsonify({"error": "Google account not connected"}), 400

        event_data = fetch_google_event_data(google_event_id, calendar_id, google_account.access_token, user_id)
        if not event_data:
            return jsonify({"error": "Failed to fetch Google event"}), 400

        google_event = GoogleEvent(
            user_id=user_id,
            google_event_id=google_event_id,
            calendar_id=calendar_id,
            title=event_data["summary"],
            start_time=event_data["start"],
            end_time=event_data["end"],
            location=event_data.get("location"),
            description=event_data.get("description")
        )
        db.session.add(google_event)
        db.session.flush()

    exists = EventAssignment.query.filter_by(customer_id=customer.id, event_id=google_event.id).first()
    if not exists:
        assignment = EventAssignment(customer_id=customer.id, event_id=google_event.id)
        db.session.add(assignment)
        db.session.commit()

    return jsonify({"message": "Assigned"}), 201


@bp.route("/api/events/unassign", methods=["POST"])
@csrf.exempt
def unassign_customer():
    email = request.args.get("user_email")
    google_event_id = request.args.get("google_event_id")
    user_id = get_user_id_from_email(email)
    if not user_id:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    customer_id = data.get("customer_id")

    customer = Customer.query.filter_by(id=customer_id, user_id=user_id).first_or_404()

    google_event = GoogleEvent.query.filter_by(user_id=user_id, google_event_id=google_event_id).first_or_404()

    assignment = EventAssignment.query.filter_by(event_id=google_event.id, customer_id=customer.id).first()
    if assignment:
        db.session.delete(assignment)
        db.session.commit()

        remaining = EventAssignment.query.filter_by(event_id=google_event.id).count()
        if remaining == 0:
            db.session.delete(google_event)
            db.session.commit()

    return jsonify({"message": "Unassigned"}), 200