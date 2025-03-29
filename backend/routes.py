from flask import Flask, jsonify
from backend.models import db  # Ensure models are imported
from flask import current_app as app

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to XeroWaste API"}), 200
