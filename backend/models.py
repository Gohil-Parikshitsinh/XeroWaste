from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 1️⃣ Users Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)    # Hashed password
    role = db.Column(db.String(50), nullable=False)  # Admin, Staff
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 2️⃣ Inventory Table
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))  # kg, liters, etc.
    category = db.Column(db.String(50), nullable=False)  # e.g., Plastic, Metal
    expiry_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 3️⃣ Waste Collection Table
class WasteCollection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collected_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    waste_type = db.Column(db.String(50), nullable=False)  # Organic, Electronic, etc.
    weight = db.Column(db.Float, nullable=False)  # in kg
    collection_date = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(255), nullable=False)

# 4️⃣ Recycling Process Table
class RecyclingProcess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waste_id = db.Column(db.Integer, db.ForeignKey('waste_collection.id'), nullable=False)
    processed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    process_type = db.Column(db.String(100), nullable=False)  # Shredding, Melting, etc.
    processed_weight = db.Column(db.Float, nullable=False)
    process_date = db.Column(db.DateTime, default=datetime.utcnow)

# 5️⃣ Disposal Records Table
class DisposalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waste_id = db.Column(db.Integer, db.ForeignKey('waste_collection.id'), nullable=False)
    disposed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    method = db.Column(db.String(100), nullable=False)  # Incineration, Landfill, etc.
    disposal_date = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(255), nullable=False)

# 6️⃣ Suppliers Table
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
