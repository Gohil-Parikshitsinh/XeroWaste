from flask import Flask, render_template

app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    # Sample data
    data = {
        "total_products": 120,
        "stock_level": 85,
        "expired_items": 7,
        "total_waste": 15,
        "recent_inventory": [
            {"name": "Product A", "quantity": 20, "expiry_date": "2025-06-01"},
            {"name": "Product B", "quantity": 5, "expiry_date": "2024-03-01"},
        ],
    }
    return render_template("dashboard.html", **data)

if __name__ == '__main__':
    app.run(debug=True)
