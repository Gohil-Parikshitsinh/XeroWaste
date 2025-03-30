from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import text

app = Flask(__name__)

# ✅ Use SQLAlchemy MySQL Connection (XAMPP on port 4306)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:4306/xerowaste"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ✅ Models
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, default=0)
    expiry_date = db.Column(db.Date, nullable=True)

    purchases = db.relationship('ProductPurchase', backref='product', lazy=True)


class ProductPurchase(db.Model):
    __tablename__ = 'product_purchases'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # ✅ Fixed FK
    quantity = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.Date, default=datetime.now)


class WasteEntry(db.Model):
    __tablename__ = "waste_entries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    waste_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(100))
    waste_date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    reason = db.Column(db.Text)

    def __repr__(self):
        return f"<WasteEntry {self.waste_type}, {self.quantity} {self.unit}>"








# ✅ Dashboard Route
@app.route('/dashboard')
def dashboard():
    products_count = Product.query.count()
    expired_items = Product.query.filter(Product.expiry_date < datetime.today()).count()
    total_waste = ProductPurchase.query.count()  # This should be calculated properly

    return render_template("dashboard.html", total_products=products_count, expired_items=expired_items,
                           total_waste=total_waste)

# ✅ Inventory Route
@app.route('/inventory')
def inventory():
    products = Product.query.all()
    return render_template("inventory.html", products=products)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        print(request.form)  # Debugging

        try:
            name = request.form['name']
            category = request.form['category']
            stock = int(request.form['stock'])
            price = float(request.form['price'])  # ✅ Ensure price is present
            expiry_date = datetime.strptime(request.form['expiry_date'], "%Y-%m-%d")
        except KeyError as e:
            return f"Missing form field: {str(e)}", 400  # Handle missing fields

        # Check if product exists
        existing_product = Product.query.filter_by(name=name).first()

        if not existing_product:
            # Create new product if not exists
            new_product = Product(name=name, category=category, stock=0, expiry_date=expiry_date)
            db.session.add(new_product)
            db.session.commit()
            product_id = new_product.id
        else:
            product_id = existing_product.id

        # Add purchase entry
        new_purchase = ProductPurchase(product_id=product_id, quantity=stock, price_per_unit=price)
        db.session.add(new_purchase)

        # Update stock
        existing_product.stock += stock
        db.session.commit()

        return redirect(url_for('inventory'))

    return render_template("add_product.html")


# ✅ Edit Product
@app.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.category = request.form['category']
        product.expiry_date = datetime.strptime(request.form['expiry_date'], "%Y-%m-%d")

        db.session.commit()
        return redirect(url_for('inventory'))

    return render_template("edit_product.html", product=product)


# ✅ Delete Product
@app.route('/delete-product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    # Delete associated purchases first
    ProductPurchase.query.filter_by(product_id=product.id).delete()

    # Delete product
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('inventory'))



@app.route("/waste-tracking")
def waste_tracking():
    waste_entries = WasteEntry.query.order_by(WasteEntry.waste_date.desc()).all()
    return render_template("waste_tracking.html", waste_entries=waste_entries)

@app.route("/add-waste", methods=["GET", "POST"])
def add_waste_entry():  # <-- Changed function name
    if request.method == "POST":
        waste_type = request.form.get("waste_type")
        quantity = float(request.form.get("quantity"))
        unit = request.form.get("unit")
        source = request.form.get("source")
        waste_date = request.form.get("waste_date")
        reason = request.form.get("reason")

        new_waste = WasteEntry(
            waste_type=waste_type,
            quantity=quantity,
            unit=unit,
            source=source,
            waste_date=waste_date,
            reason=reason
        )

        db.session.add(new_waste)
        db.session.commit()
        return redirect(url_for("waste_tracking"))

    return render_template("add_waste.html")

@app.route("/waste-analysis")
def waste_analysis():
    # ✅ Fetch waste data from waste_entries
    waste_entries_query = text("SELECT source, SUM(quantity) as total FROM waste_entries GROUP BY source")
    waste_entries = db.session.execute(waste_entries_query).fetchall()

    # ✅ Fetch expired products as waste
    expired_products_query = text("SELECT category, SUM(stock) as total FROM products WHERE expiry_date < CURDATE() GROUP BY category")
    expired_products = db.session.execute(expired_products_query).fetchall()

    # ✅ Combine both sources into a single dictionary
    waste_data = {}

    # Add manually logged waste
    for row in waste_entries:
        source, total = row
        waste_data[source] = total

    # Add expired products as waste (either merge or create new entry)
    for row in expired_products:
        category, total = row
        if category in waste_data:
            waste_data[category] += total  # Merge if source exists
        else:
            waste_data[category] = total  # Add new source

    print("Final Waste Breakdown:", waste_data)  # Debugging

    return render_template("waste_analysis.html", waste_breakdown=waste_data)

if __name__ == '__main__':
    app.run(debug=True)
