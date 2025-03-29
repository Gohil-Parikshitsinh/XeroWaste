from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# ✅ Initialize Flask App
app = Flask(__name__)

# ✅ Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:4306/XeroWaste'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

# ✅ Initialize Database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)










# ✅ User Model (Table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')



# ✅ Create tables before running
with app.app_context():
    db.create_all()





















@app.route('/')
def home():
    return render_template('layout.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # ✅ Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "User already exists!", 400

        # ✅ Add new user
        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # ✅ Fetch user from DB
        user = User.query.filter_by(email=email).first()

        # ✅ Verify password
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return "Login Successful!"  # Replace with redirect to dashboard
        return "Invalid Credentials!", 401

    return render_template('login.html')


# ✅ User Management Routes (Testing)
@app.route('/users', methods=['GET'])
def get_users():
    return "Fetch all users"

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return f"Fetch details of user {id}"

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    return f"Update user {id}"

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    return f"Delete user {id}"

# ✅ Waste Collection Routes (Testing)
@app.route('/waste/request', methods=['POST'])
def request_waste_pickup():
    return "Request waste pickup"

@app.route('/waste/status/<int:request_id>', methods=['GET'])
def check_waste_status(request_id):
    return f"Status of waste request {request_id}"

@app.route('/waste/collections', methods=['GET'])
def get_waste_collections():
    return "Fetch all waste collection requests"

# ✅ Recycling Routes (Testing)
@app.route('/recycling-centers', methods=['GET'])
def get_recycling_centers():
    return "Fetch all recycling centers"

@app.route('/recycling-items', methods=['GET'])
def get_recycling_items():
    return "List of recyclable items"

@app.route('/recycling/submit', methods=['POST'])
def submit_recycling():
    return "Submit items for recycling"

# ✅ Reporting Routes (Testing)
@app.route('/reports', methods=['GET'])
def get_reports():
    return "Fetch all reports"

@app.route('/report', methods=['POST'])
def submit_report():
    return "Submit a waste-related report"

if __name__ == '__main__':
    print(app.url_map)  # ✅ Debugging: Check registered routes
    app.run(debug=True)
