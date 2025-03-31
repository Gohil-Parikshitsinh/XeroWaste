from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import text

app = Flask(__name__)

# ✅ Use SQLAlchemy MySQL Connection (XAMPP on port 4306)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:4306/xerowaste"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"

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


class Dishes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)


# ✅ Ingredient Model
class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    unit = db.Column(db.String(50), nullable=False)

# ✅ Dish-Ingredient Mapping Model
class DishIngredient(db.Model):
    __tablename__ = "dish_ingredients"
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey("dishes.id"), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"), nullable=False)
    quantity_used = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(50), nullable=False)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_paid = db.Column(db.Boolean, default=False)

class Tables(db.Model):
    id = db.Column(db.Integer, primary_key=True)





@app.route('/')
def index():
    return render_template("index.html")
@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/demo')
def demo():
    return render_template("demo.html")
@app.route('/features')
def features():
    return render_template("features.html")
@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/pricing')
def pricing():
    return render_template("pricing.html")

@app.route('/privacy')
def privacy():
    return render_template("privacy.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/dashboard')
def dashboard():
    # ✅ Get Total Products
    products_count = Product.query.count()

    # ✅ Get Expired Products
    expired_products = Product.query.filter(Product.expiry_date < datetime.today()).all()
    expired_items = len(expired_products)

    # ✅ Total Waste Entries
    total_waste = WasteEntry.query.count()  # Fixed waste calculation

    return render_template(
        "dashboard.html",
        total_products=products_count,
        expired_items=expired_items,
        total_waste=total_waste,
        expired_products=expired_products  # Send expired products to the template
    )

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








@app.route("/menu")
def menu():
    dishes = db.session.execute(
        text("SELECT id, name, price, image_url FROM dishes")  # ✅ Add image_url
    ).fetchall()

    ingredients = db.session.execute(
        text("""
            SELECT dish_ingredients.dish_id, ingredients.name, dish_ingredients.quantity_used, ingredients.unit
            FROM dish_ingredients
            JOIN ingredients ON dish_ingredients.ingredient_id = ingredients.id
        """)
    ).fetchall()

    # Organize ingredients by dish_id
    dish_ingredient_map = {}
    for row in ingredients:
        dish_id, name, quantity_used, unit = row
        if dish_id not in dish_ingredient_map:
            dish_ingredient_map[dish_id] = []
        dish_ingredient_map[dish_id].append((name, quantity_used, unit))

    return render_template("menu.html", dishes=dishes, dish_ingredient_map=dish_ingredient_map)

# ✅ Add New Dish
@app.route("/add_dish", methods=["POST"])
def add_dish():
    name = request.form.get("name")
    price = request.form.get("price")

    if name and price:
        new_dish = Dishes(name=name, price=price)
        db.session.add(new_dish)
        db.session.commit()
        flash("Dish added successfully!", "success")
    else:
        flash("Failed to add dish. Please provide all details.", "danger")

    return redirect(url_for("menu"))

@app.route("/sell_dish", methods=["POST"])
def sell_dish():
    dish_id = request.form.get("dish_id")
    table_id = request.form.get("table_id")  # New: Assign order to a table
    quantity = int(request.form.get("quantity", 1))

    dish_ingredients = DishIngredient.query.filter_by(dish_id=dish_id).all()

    for dish_ingredient in dish_ingredients:
        ingredient = Ingredient.query.get(dish_ingredient.ingredient_id)

        if ingredient.stock < dish_ingredient.quantity_used * quantity:
            flash(f"Not enough {ingredient.name} in stock!", "danger")
            return redirect(url_for("menu"))

    # If all ingredients are available, deduct stock
    for dish_ingredient in dish_ingredients:
        ingredient = Ingredient.query.get(dish_ingredient.ingredient_id)
        ingredient.stock -= dish_ingredient.quantity_used * quantity

    # Save Order Record with table_id
    new_order = Orders(dish_id=dish_id, table_id=table_id, quantity=quantity)
    db.session.add(new_order)

    # Mark table as occupied
    table = Tables.query.get(table_id)
    if table:
        table.status = "Occupied"

    db.session.commit()
    flash("Dish sold successfully!", "success")

    return redirect(url_for("menu"))


@app.route('/order', methods=['POST'])
def place_order():
    table_id = request.form.get('table_id')
    dish_id = request.form.get('dish_id')
    quantity = request.form.get('quantity')

    new_order = Orders(table_id=table_id, dish_id=dish_id, quantity=quantity)
    db.session.add(new_order)

    # Mark table as "Occupied"
    table = Tables.query.get(table_id)
    if table:
        table.status = "Occupied"

    db.session.commit()
    return redirect(url_for('menu'))

@app.route('/table/<int:table_id>/orders')
def table_orders(table_id):
    table = Tables.query.get_or_404(table_id)

    orders = db.session.execute(
        text("""
            SELECT orders.id, dishes.name, orders.quantity, orders.order_date
            FROM orders
            JOIN dishes ON orders.dish_id = dishes.id
            WHERE orders.table_id = :table_id
        """),
        {"table_id": table_id}
    ).fetchall()

    return render_template('table_orders.html', table=table, orders=orders)


@app.route("/bill/<int:table_id>")
def generate_bill(table_id):
    table = Tables.query.get_or_404(table_id)

    orders = db.session.execute(
        text("""
            SELECT orders.id, dishes.name, dishes.price, orders.quantity
            FROM orders
            JOIN dishes ON orders.dish_id = dishes.id
            WHERE orders.table_id = :table_id
        """),
        {"table_id": table_id}
    ).fetchall()

    total_price = sum(order[2] * order[3] for order in orders)  # order[2] = price, order[3] = quantity

    return render_template("bill.html", orders=orders, total_price=total_price, table=table)



if __name__ == '__main__':
    app.run(debug=True)
