import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "eshop_dynamic.db")
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open(SCHEMA_FILE, "r") as f:
        conn.executescript(f.read())
    # Safe column migrations for existing databases
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE upi_configs ADD COLUMN qr_image TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN payment_method TEXT DEFAULT 'QR_UPI'")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN utr_number TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN payment_status TEXT DEFAULT 'CONFIRMED'")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()
    seed_initial_data()

def seed_initial_data():
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Admin User
    cursor.execute("SELECT id FROM users WHERE email = ?", ("admin@gmail.com",))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (email, password, first_name, last_name, role, phone, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("admin@gmail.com", "admin", "System", "Admin", "admin", "9999999999", "Headquarters"))

    # 2. Test Customer User
    cursor.execute("SELECT id FROM users WHERE email = ?", ("user@gmail.com",))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (email, password, first_name, last_name, role, phone, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("user@gmail.com", "user123", "John", "Doe", "user", "9876543210", "123 Main Street"))

    # 3. Initial UPI Config
    cursor.execute("SELECT id FROM upi_configs")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO upi_configs (upi_id, payee_name, is_active)
            VALUES (?, ?, ?)
        """, ("eashop@upi", "E-AIShop Store", 1))

    # 4. Categories
    cursor.execute("DELETE FROM categories")
    categories = [
        ("CAT_COSTUMES", "Costumes & Fashion Try-On", "IMG_CAT_COSTUMES"),
        ("CAT_LAPTOP", "Laptops & Computers", "IMG_CAT_LAPTOP"),
        ("CAT_SMARTPHONE", "Smartphones & Tablets", "IMG_CAT_PHONE"),
        ("CAT_AUDIO", "Audio & Headphones", "IMG_CAT_AUDIO"),
        ("CAT_ACCESSORY", "Accessories & Wearables", "IMG_CAT_ACCESSORY"),
    ]
    cursor.executemany("""
        INSERT INTO categories (category_id_str, category_name, image_id)
        VALUES (?, ?, ?)
    """, categories)

    # 5. Products including 4 Try-On Costumes and Tech
    cursor.execute("DELETE FROM products")
    products = [
        # Try-On Costumes / Outfits
        ("IMG_PROD_COSTUME_01", "Royal Tuxedo & Suit", "VogueCraft", "Classic black velvet slim-fit tuxedo with silk lapel and tailored pants. Perfect for galas and formal events.", 4999.0, 3499.0, 20, 1),
        ("IMG_PROD_COSTUME_02", "Cyberpunk Neon Jacket", "FutureWear", "High-tech street style cyberpunk jacket with glowing neon accents and weather-resistant fiber.", 3999.0, 2899.0, 15, 1),
        ("IMG_PROD_COSTUME_03", "Traditional Silk Kurta Sherwani", "RoyalEthnic", "Handcrafted embroidered designer sherwani with regal gold zari motifs.", 5499.0, 3999.0, 18, 1),
        ("IMG_PROD_COSTUME_04", "Cosmic Superhero Armor Suit", "HeroGear", "Ergonomic composite superhero armor suit with dynamic chest plate and breathable mesh.", 6499.0, 4499.0, 12, 1),
        
        # Tech Products
        ("IMG_PROD_LAPTOP_01", "UltraSlim Pro Laptop 15", "TechCorp", "High performance Intel i7 laptop with 16GB RAM and 512GB SSD.", 75000.0, 64999.0, 15, 2),
        ("IMG_PROD_PHONE_01", "Galaxy X 5G Smartphone", "MobileTech", "AMOLED display, 108MP camera, 128GB storage with fast charging.", 55000.0, 48999.0, 20, 3),
        ("IMG_PROD_AUDIO_01", "Noise-Cancelling Wireless Headphones", "SoundMaster", "Active Noise Cancelling over-ear headphones with 30h battery.", 14999.0, 9999.0, 30, 4),
        ("IMG_PROD_WATCH_01", "Smart Fitness Watch 4", "FitPulse", "Heart rate tracker, GPS, AMOLED always-on display, water resistant.", 8999.0, 5999.0, 25, 5),
        ("IMG_PROD_LAPTOP_02", "Gaming Beast RGB Laptop", "TechCorp", "RTX 4060 graphics, Ryzen 7, 144Hz IPS Gaming screen.", 98000.0, 89990.0, 10, 2),
        ("IMG_PROD_AUDIO_02", "True Wireless Earbuds", "SoundMaster", "Bluetooth 5.3 earbuds with deep bass and fast wireless charging case.", 3999.0, 2499.0, 50, 4),
    ]
    cursor.executemany("""
        INSERT INTO products (image_id, product_name, company_name, description, price, discounted_price, stock, category_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, products)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized & seeded successfully with costumes and dynamic inventory!")
