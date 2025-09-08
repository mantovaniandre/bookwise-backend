from flask import Blueprint, request, jsonify
from demo_data import DEMO_USERS, DEMO_BOOKS, DEMO_CART

demo_route = Blueprint("demo_route", __name__)

@demo_route.route("/demo/books", methods=["GET"])
def get_demo_books():
    """Get all demo books"""
    return jsonify({"books": DEMO_BOOKS}), 200

@demo_route.route("/demo/login", methods=["POST"])  
def demo_login():
    """Demo login - works with multiple users"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Check if user exists and password matches
    if email in DEMO_USERS and DEMO_USERS[email]["password"] == password:
        return jsonify({
            "message": "Login successful!",
            "user": DEMO_USERS[email],
            "token": "demo_token_12345"
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@demo_route.route("/login", methods=["POST"])  
def frontend_login():
    """Login endpoint for frontend compatibility"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Check if user exists and password matches
    if email in DEMO_USERS and DEMO_USERS[email]["password"] == password:
        return jsonify({
            "message": "Login successful!",
            "user": DEMO_USERS[email],
            "token": "demo_token_12345"
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@demo_route.route("/demo/register", methods=["POST"])
def demo_register():
    """Demo registration - always succeeds"""
    return jsonify({"message": "Registration successful! You can now login with admin@bookwise.com"}), 201

@demo_route.route("/createUser", methods=["POST"])
def frontend_register():
    """Registration endpoint for frontend compatibility"""
    return jsonify({"message": "Registration successful! You can now login with admin@bookwise.com"}), 201

@demo_route.route("/demo/cart", methods=["GET", "POST"])
def demo_cart():
    """Demo cart operations"""
    if request.method == "GET":
        # Return empty cart or current cart
        cart_items = DEMO_CART.get("demo_user", [])
        return jsonify({"cart_items": cart_items}), 200
    
    elif request.method == "POST":
        # Add item to cart
        data = request.get_json()
        book_id = data.get('book_id')
        quantity = data.get('quantity', 1)
        
        # Find the book
        book = next((b for b in DEMO_BOOKS if b["id"] == str(book_id)), None)
        if book:
            # Add to demo cart
            if "demo_user" not in DEMO_CART:
                DEMO_CART["demo_user"] = []
            
            # Check if item already in cart
            existing_item = next((item for item in DEMO_CART["demo_user"] if item["id"] == book["id"]), None)
            if existing_item:
                existing_item["quantity"] += quantity
            else:
                cart_item = {
                    "id": book["id"],
                    "title": book["title"], 
                    "price": book["price"],
                    "quantity": quantity,
                    "url_img": book["url_img"],
                    "stock": book["stock"]
                }
                DEMO_CART["demo_user"].append(cart_item)
            
            return jsonify({"message": "Item added to cart successfully!"}), 200
        else:
            return jsonify({"message": "Book not found"}), 404

# Frontend compatibility endpoints
@demo_route.route("/api/books", methods=["GET"])
def get_books_for_frontend():
    """Get all books for frontend compatibility with pagination support"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Simple pagination simulation (since we have a small dataset)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_books = DEMO_BOOKS[start:end] if start < len(DEMO_BOOKS) else []
    
    return jsonify({
        "books": paginated_books,
        "total": len(DEMO_BOOKS),
        "page": page,
        "per_page": per_page
    }), 200

@demo_route.route("/api/books/featured", methods=["GET"])
def get_featured_books():
    """Get featured books"""
    featured = [book for book in DEMO_BOOKS if book.get("featured", False)]
    return jsonify({"books": featured}), 200

@demo_route.route("/api/books/bestsellers", methods=["GET"])
def get_bestsellers():
    """Get bestseller books"""
    bestsellers = [book for book in DEMO_BOOKS if book.get("bestseller", False)]
    return jsonify({"books": bestsellers}), 200

@demo_route.route("/api/categories", methods=["GET"])
def get_categories():
    """Get book categories"""
    return jsonify({"categories": ["Programming", "Technology", "Software Development"]}), 200

@demo_route.route("/api/books/<book_id>", methods=["GET"])
def get_book_by_id(book_id):
    """Get book by ID"""
    book = next((b for b in DEMO_BOOKS if b["id"] == book_id), None)
    if book:
        return jsonify({"book": book}), 200
    else:
        return jsonify({"message": "Book not found"}), 404

@demo_route.route("/api/books/search", methods=["GET"])
def search_books():
    """Search books by option and term"""
    option = request.args.get('option', '')
    term = request.args.get('term', '')
    
    if not option or not term:
        return jsonify({"books": []}), 200
    
    results = []
    for book in DEMO_BOOKS:
        if option == 'title' and term.lower() in book['title'].lower():
            results.append(book)
        elif option == 'author' and term.lower() in book['author'].lower():
            results.append(book)
        elif option == 'language' and term.lower() in book['language'].lower():
            results.append(book)
        elif option == 'category' and term.lower() in book['category'].lower():
            results.append(book)
    
    return jsonify({"books": results}), 200

# User profile and management endpoints
@demo_route.route("/profileUser", methods=["GET"])
def get_user_profile():
    """Get user profile - returns demo client user"""
    return jsonify({
        "user": DEMO_USERS["client@bookwise.com"],
        "message": "Profile retrieved successfully"
    }), 200

@demo_route.route("/updateUser", methods=["PUT"])
def update_user():
    """Update user - always succeeds"""
    return jsonify({"message": "User updated successfully!"}), 200

@demo_route.route("/deleteUser", methods=["DELETE"])
def delete_user():
    """Delete user - always succeeds"""
    return jsonify({"message": "User deleted successfully!"}), 200

# Cart endpoints
@demo_route.route("/api/cart/items", methods=["GET"])
def get_cart_items():
    """Get cart items"""
    cart_items = DEMO_CART.get("demo_user", [])
    return jsonify({"cart_items": cart_items}), 200

@demo_route.route("/api/cart/items", methods=["POST"])
def add_cart_item():
    """Add item to cart"""
    data = request.get_json()
    book_id = data.get('book_id')
    quantity = data.get('quantity', 1)
    
    # Find the book
    book = next((b for b in DEMO_BOOKS if b["id"] == str(book_id)), None)
    if book:
        # Add to demo cart
        if "demo_user" not in DEMO_CART:
            DEMO_CART["demo_user"] = []
        
        # Check if item already in cart
        existing_item = next((item for item in DEMO_CART["demo_user"] if item["id"] == book["id"]), None)
        if existing_item:
            existing_item["quantity"] += quantity
        else:
            cart_item = {
                "id": book["id"],
                "title": book["title"], 
                "price": book["price"],
                "quantity": quantity,
                "url_img": book["url_img"],
                "stock": book["stock"]
            }
            DEMO_CART["demo_user"].append(cart_item)
        
        return jsonify({"message": "Item added to cart successfully!"}), 200
    else:
        return jsonify({"message": "Book not found"}), 404

@demo_route.route("/api/cart/items/<item_id>", methods=["DELETE"])
def remove_cart_item(item_id):
    """Remove item from cart"""
    if "demo_user" in DEMO_CART:
        DEMO_CART["demo_user"] = [item for item in DEMO_CART["demo_user"] if item["id"] != item_id]
    return jsonify({"message": "Item removed from cart"}), 200

# Purchase/Order endpoints
@demo_route.route("/createPurchase", methods=["POST"])
def create_purchase():
    """Create purchase - always succeeds"""
    return jsonify({"message": "Purchase created successfully!", "order_id": "demo_order_123"}), 201

@demo_route.route("/getPurchase", methods=["GET"])
def get_purchases():
    """Get user purchases"""
    demo_purchases = [
        {
            "id": "1",
            "order_number": "ORD-001",
            "total": "45.99",
            "status": "completed",
            "date": "2024-01-15",
            "items": [{"title": "Clean Code", "quantity": 1, "price": "45.99"}]
        }
    ]
    return jsonify({"purchases": demo_purchases}), 200

# Payment endpoints
@demo_route.route("/api/payments/create-intent", methods=["POST"])
def create_payment_intent():
    """Create payment intent"""
    return jsonify({
        "client_secret": "demo_payment_intent_12345",
        "message": "Payment intent created successfully"
    }), 200

# Order endpoints
@demo_route.route("/api/orders", methods=["GET"])
def get_orders():
    """Get user orders"""
    demo_orders = [
        {
            "id": "1",
            "order_number": "ORD-001",
            "total": "45.99",
            "status": "completed",
            "created_at": "2024-01-15T10:00:00Z"
        }
    ]
    return jsonify({"orders": demo_orders}), 200

@demo_route.route("/api/orders", methods=["POST"])
def create_order():
    """Create new order"""
    return jsonify({
        "message": "Order created successfully!",
        "order": {
            "id": "demo_order_456",
            "order_number": "ORD-002",
            "status": "pending"
        }
    }), 201