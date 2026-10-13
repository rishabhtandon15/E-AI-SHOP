from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import sqlite3
import os
import uuid
import random
import re
from database import get_db, init_db
from neurosymbolic_engine import execute_neurosymbolic_reasoning, PRODUCT_ONTOLOGY, find_symbolic_product

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
except ImportError:
    pass

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests for Flutter Web & Mobile

# Ensure database is initialized on startup
init_db()

# High quality product & category image mapping dictionary
IMAGE_MAP = {
    # Costume Outfits for Virtual Try-On
    "IMG_PROD_COSTUME_01": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=600&q=80",  # Royal Tuxedo & Suit
    "IMG_PROD_COSTUME_02": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&q=80",  # Cyberpunk Neon Jacket
    "IMG_PROD_COSTUME_03": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=600&q=80",  # Traditional Silk Kurta Sherwani
    "IMG_PROD_COSTUME_04": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&q=80",  # Superhero Armor Suit
    
    # Tech Product Images
    "IMG_PROD_LAPTOP_01": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&q=80", # UltraSlim Laptop
    "IMG_PROD_PHONE_01": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&q=80",  # Galaxy 5G Phone
    "IMG_PROD_AUDIO_01": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80",  # Headphones
    "IMG_PROD_WATCH_01": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80",  # Smart Watch
    "IMG_PROD_LAPTOP_02": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500&q=80", # Gaming Laptop
    "IMG_PROD_AUDIO_02": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&q=80",  # Wireless Earbuds
    
    # Category Images
    "IMG_CAT_COSTUMES": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=500&q=80",
    "IMG_CAT_LAPTOP": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&q=80",
    "IMG_CAT_PHONE": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&q=80",
    "IMG_CAT_AUDIO": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500&q=80",
    "IMG_CAT_ACCESSORY": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&q=80",
}

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500&q=80"

# ==================== IMAGE ID API ====================

@app.route('/api/images/<image_id>', methods=['GET'])
def get_image(image_id):
    url = IMAGE_MAP.get(image_id, DEFAULT_IMAGE)
    return redirect(url)

# ==================== AUTH API ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
        
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'status': 'success',
            'user': {
                'id': user['id'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'role': user['role'],
                'phone': user['phone'],
                'address': user['address']
            }
        })
    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    phone = data.get('phone', '')
    address = data.get('address', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
        
    conn = get_db()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return jsonify({'error': 'User with this email already exists'}), 400
        
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (email, password, first_name, last_name, role, phone, address)
        VALUES (?, ?, ?, ?, 'user', ?, ?)
    """, (email, password, first_name, last_name, phone, address))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'status': 'success',
        'message': 'Account created successfully',
        'user': {
            'id': user_id,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'role': 'user'
        }
    })

# ==================== PRODUCTS & CATEGORIES API ====================

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db()
    categories = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    return jsonify([dict(c) for c in categories])


@app.route('/api/products', methods=['GET'])
def get_products():
    search = request.args.get('search', '').strip()
    category_id = request.args.get('category_id')
    
    conn = get_db()
    query = "SELECT p.*, c.category_name FROM products p LEFT JOIN categories c ON p.category_id = c.id WHERE p.is_active = 1"
    params = []
    
    if category_id:
        query += " AND p.category_id = ?"
        params.append(category_id)
        
    if search:
        query += " AND (p.product_name LIKE ? OR p.company_name LIKE ? OR p.description LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])
        
    query += " ORDER BY p.id DESC"
    products = conn.execute(query, params).fetchall()
    conn.close()
    
    result = []
    for p in products:
        p_dict = dict(p)
        sym = PRODUCT_ONTOLOGY.get(p_dict.get('image_id'))
        if sym:
            p_dict['rating'] = sym.get('rating', 4.8)
            p_dict['specs'] = sym.get('specs_table', {})
            p_dict['highlights'] = sym.get('highlights', [])
            p_dict['suitable_for'] = sym.get('suitable_for', [])
            p_dict['warranty'] = sym.get('warranty', '')
            p_dict['delivery_days'] = sym.get('delivery_days', '2-3 Business Days')
        result.append(p_dict)
    return jsonify(result)


@app.route('/api/products/search-preview', methods=['GET'])
def search_preview():
    """Fast dynamic preview search endpoint returning product suggestions with image, price, and category."""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    conn = get_db()
    sql = """
        SELECT p.id, p.image_id, p.product_name, p.company_name, p.discounted_price, p.price, p.category_id, c.category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = 1 AND (p.product_name LIKE ? OR p.company_name LIKE ? OR p.description LIKE ?)
        LIMIT 6
    """
    term = f"%{query}%"
    rows = conn.execute(sql, (term, term, term)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_detail(product_id):
    conn = get_db()
    product = conn.execute("SELECT p.*, c.category_name FROM products p LEFT JOIN categories c ON p.category_id = c.id WHERE p.id = ?", (product_id,)).fetchone()
    conn.close()
    if product:
        prod_dict = dict(product)
        sym = PRODUCT_ONTOLOGY.get(prod_dict.get('image_id'))
        if sym:
            prod_dict['rating'] = sym.get('rating', 4.8)
            prod_dict['specs'] = sym.get('specs_table', {})
            prod_dict['highlights'] = sym.get('highlights', [])
            prod_dict['suitable_for'] = sym.get('suitable_for', [])
            prod_dict['warranty'] = sym.get('warranty', '')
            prod_dict['delivery_days'] = sym.get('delivery_days', '2-3 Business Days')
        return jsonify(prod_dict)
    return jsonify({'error': 'Product not found'}), 404

# ==================== CART API ====================

@app.route('/api/cart', methods=['GET'])
def get_cart():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
        
    conn = get_db()
    items = conn.execute("""
        SELECT c.id as cart_id, c.quantity, p.*
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,)).fetchall()
    conn.close()
    
    cart_items = [dict(item) for item in items]
    total = sum(item['discounted_price'] * item['quantity'] for item in cart_items)
    return jsonify({'items': cart_items, 'total_amount': total, 'total_count': len(cart_items)})


@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not user_id or not product_id:
        return jsonify({'error': 'user_id and product_id required'}), 400
        
    conn = get_db()
    existing = conn.execute("SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id)).fetchone()
    
    cursor = conn.cursor()
    if existing:
        cursor.execute("UPDATE cart SET quantity = quantity + ? WHERE id = ?", (quantity, existing['id']))
    else:
        cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)", (user_id, product_id, quantity))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Item added to cart'})


@app.route('/api/cart/update', methods=['PUT'])
def update_cart_quantity():
    data = request.get_json() or {}
    cart_id = data.get('cart_id')
    quantity = data.get('quantity')
    
    if not cart_id or quantity is None:
        return jsonify({'error': 'cart_id and quantity required'}), 400
        
    conn = get_db()
    cursor = conn.cursor()
    if quantity <= 0:
        cursor.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
    else:
        cursor.execute("UPDATE cart SET quantity = ? WHERE id = ?", (quantity, cart_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Cart updated'})

# ==================== ORDERS API ====================

@app.route('/api/orders', methods=['GET'])
def get_orders():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    conn = get_db()
    orders = conn.execute("""
        SELECT o.* FROM orders o
        WHERE o.user_id = ?
        ORDER BY o.id DESC
    """, (user_id,)).fetchall()

    result = []
    for o in orders:
        items = conn.execute("""
            SELECT oi.*, p.product_name, p.image_id, p.company_name
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        """, (o['id'],)).fetchall()
        ord_dict = dict(o)
        ord_dict['items'] = [dict(i) for i in items]
        result.append(ord_dict)

    conn.close()
    return jsonify(result)


@app.route('/api/orders/place', methods=['POST'])
def place_order():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    shipping_address = data.get('shipping_address', '')
    phone = data.get('phone', '')
    utr_number = data.get('utr_number', '')

    if not user_id:
        return jsonify({'error': 'user_id required'}), 400

    conn = get_db()
    cart_items = conn.execute("""
        SELECT c.*, p.discounted_price, p.product_name
        FROM cart c JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,)).fetchall()

    if not cart_items:
        conn.close()
        return jsonify({'error': 'Cart is empty'}), 400

    total_amount = sum(item['discounted_price'] * item['quantity'] for item in cart_items)
    track_id = f"TRK-{uuid.uuid4().hex[:8].upper()}"

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (track_id, user_id, total_amount, status, shipping_address, phone, payment_method, utr_number, payment_status)
        VALUES (?, ?, ?, 1, ?, ?, 'QR_UPI', ?, 'CONFIRMED')
    """, (track_id, user_id, total_amount, shipping_address, phone, utr_number))
    order_id = cursor.lastrowid

    for item in cart_items:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        """, (order_id, item['product_id'], item['quantity'], item['discounted_price']))

    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({
        'status': 'success',
        'track_id': track_id,
        'total_amount': total_amount,
        'message': 'Order successfully placed!'
    })


@app.route('/api/orders/<track_id>/update-status', methods=['PUT'])
def update_order_status(track_id):
    data = request.get_json() or {}
    new_status = data.get('status')

    if not new_status:
        return jsonify({'error': 'status required'}), 400
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE track_id = ?", (new_status, track_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': f'Order status updated to {new_status}'})


# ==================== ADMIN DYNAMIC UPI & QR CODE API ====================

@app.route('/api/admin/upi', methods=['GET'])
def get_upi_configs():
    conn = get_db()
    upis = conn.execute("SELECT * FROM upi_configs ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(u) for u in upis])


@app.route('/api/admin/upi/active', methods=['GET'])
def get_active_upi():
    conn = get_db()
    active_upi = conn.execute("SELECT * FROM upi_configs WHERE is_active = 1 ORDER BY id DESC").fetchone()
    conn.close()
    if active_upi:
        return jsonify(dict(active_upi))
    return jsonify({
        'upi_id': 'admin@upi',
        'payee_name': 'E-AIShop Store',
        'qr_image': ''
    })


@app.route('/api/admin/upi', methods=['POST'])
def add_upi():
    data = request.get_json() or {}
    qr_image = data.get('qr_image', '')
    upi_id = data.get('upi_id', 'Store QR Account')
    payee_name = data.get('payee_name', 'Merchant Store')
    set_active = data.get('set_active', True)
    
    if not qr_image and not upi_id:
        return jsonify({'error': 'QR image is required'}), 400
        
    conn = get_db()
    cursor = conn.cursor()
    if set_active:
        cursor.execute("UPDATE upi_configs SET is_active = 0")
        
    cursor.execute("""
        INSERT INTO upi_configs (upi_id, payee_name, qr_image, is_active)
        VALUES (?, ?, ?, ?)
    """, (upi_id, payee_name, qr_image, 1 if set_active else 0))
    
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Payment QR uploaded & activated successfully'})


@app.route('/api/admin/upi/<int:upi_id_num>', methods=['DELETE'])
def delete_upi(upi_id_num):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM upi_configs WHERE id = ?", (upi_id_num,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Payment QR deleted'})

# ==================== ADMIN PRODUCT & ORDER API ====================

@app.route('/api/admin/products', methods=['POST'])
def add_product():
    data = request.get_json() or {}
    name = data.get('product_name')
    company = data.get('company_name', 'Generic')
    desc = data.get('description', '')
    price = float(data.get('price', 0))
    disc_price = float(data.get('discounted_price', price))
    stock = int(data.get('stock', 10))
    cat_id = int(data.get('category_id', 1))
    image_id = data.get('image_id', 'IMG_PROD_LAPTOP_01')

    if not name or price <= 0:
        return jsonify({'error': 'Valid product name and price required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (image_id, product_name, company_name, description, price, discounted_price, stock, category_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (image_id, name, company, desc, price, disc_price, stock, cat_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Product added successfully'})


@app.route('/api/admin/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET is_active = 0 WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Product deleted successfully'})


@app.route('/api/admin/orders', methods=['GET'])
def get_all_orders():
    conn = get_db()
    orders = conn.execute("""
        SELECT o.*, u.email as user_email, u.first_name, u.last_name 
        FROM orders o
        LEFT JOIN users u ON o.user_id = u.id
        ORDER BY o.id DESC
    """).fetchall()
    
    result = []
    for o in orders:
        items = conn.execute("""
            SELECT oi.*, p.product_name 
            FROM order_items oi 
            JOIN products p ON oi.product_id = p.id 
            WHERE oi.order_id = ?
        """, (o['id'],)).fetchall()
        
        ord_dict = dict(o)
        ord_dict['items'] = [dict(i) for i in items]
        result.append(ord_dict)
        
    conn.close()
    return jsonify(result)


# ==================== ADVANCED NEUROSYMBOLIC AI CHATBOT API ====================

@app.route('/api/chat', methods=['POST'])
def chat_bot():
    data = request.get_json() or {}
    user_query = data.get('query', '').strip()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    product_data = data.get('product')

    conn = get_db()

    # 1. Resolve target product context if specified or referenced
    target_product = None
    if product_data and isinstance(product_data, dict):
        target_product = product_data
    elif product_id:
        row = conn.execute(
            'SELECT p.*, c.category_name FROM products p LEFT JOIN categories c ON p.category_id = c.id WHERE p.id = ?',
            (product_id,)
        ).fetchone()
        if row:
            target_product = dict(row)

    # 2. Auto-detect specific product if query directly mentions one and no focus is set
    if not target_product and user_query:
        all_prods = conn.execute(
            'SELECT p.*, c.category_name FROM products p LEFT JOIN categories c ON p.category_id = c.id WHERE p.is_active = 1'
        ).fetchall()
        for p in all_prods:
            p_dict = dict(p)
            p_name = p_dict['product_name'].lower()
            if p_name in user_query.lower() or (len(p_name.split()) >= 2 and all(w in user_query.lower() for w in p_name.split()[:2])):
                target_product = p_dict
                break

    # 3. Execute Neurosymbolic Reasoning Pipeline
    response_data = execute_neurosymbolic_reasoning(
        user_query=user_query,
        target_product=target_product,
        user_id=user_id,
        db_conn=conn
    )
    conn.close()
    return jsonify(response_data)


if __name__ == '__main__':
    print("Starting E-AIShop Python SQL Backend Server on http://127.0.0.1:5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
