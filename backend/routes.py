from flask import Flask, render_template
from backend.models import db  # Ensure models are imported
from flask import current_app as app

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
