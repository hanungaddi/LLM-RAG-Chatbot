import sqlite3
import hashlib
from datetime import datetime, timedelta
import os

# --- KONFIGURASI ---
DB_FILE = "db/toko_online.db"

# Hapus file database lama jika ada, untuk memastikan data selalu fresh
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"File database '{DB_FILE}' yang lama telah dihapus.")

# Fungsi untuk hash password (simulasi)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- KONEKSI DATABASE ---
try:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    print(f"Database '{DB_FILE}' berhasil dibuat dan koneksi berhasil.")
    
    # Aktifkan foreign key constraint
    cursor.execute("PRAGMA foreign_keys = ON;")

    # --- PEMBUATAN SKEMA TABEL ---
    print("Membuat skema tabel...")
    
    # Menggunakan TEXT untuk VARCHAR/TIMESTAMP dan REAL untuk DECIMAL di SQLite
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            phone_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS addresses (
            address_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            address_line TEXT NOT NULL,
            city TEXT NOT NULL,
            province TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            is_default BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS product_categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            category_id INTEGER,
            warranty_info TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES product_categories(category_id)
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            shipping_address_id INTEGER NOT NULL,
            tracking_number TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (shipping_address_id) REFERENCES addresses(address_id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );

        CREATE TABLE IF NOT EXISTS order_tracking (
            tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            status_update TEXT NOT NULL,
            location TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        );
    """)
    print("Skema tabel berhasil dibuat.")

    # --- PENGISIAN DATA DUMMY ---
    print("Memasukkan data dummy...")

    # Data untuk tabel users
    users_data = [
        (1, 'Budi Santoso', 'budi.s@example.com', hash_password('password123'), '081234567890'),
        (2, 'Citra Lestari', 'citra.l@example.com', hash_password('amanbanget'), '085678901234'),
        (3, 'Agus Wijaya', 'agus.w@example.com', hash_password('qwerty'), '087811223344')
    ]
    cursor.executemany("INSERT INTO users (user_id, full_name, email, password_hash, phone_number) VALUES (?, ?, ?, ?, ?)", users_data)

    # Data untuk tabel addresses
    addresses_data = [
        (1, 1, 'Jl. Merdeka No. 10, Kel. Cihampelas', 'Bandung', 'Jawa Barat', '40131', 1),
        (2, 2, 'Jl. Sudirman Kav. 5, Apartemen Sejahtera Lt. 15', 'Jakarta Selatan', 'DKI Jakarta', '12190', 1),
        (3, 1, 'Kantor PT. Maju Mundur, Jl. Gatot Subroto No. 12', 'Bandung', 'Jawa Barat', '40266', 0)
    ]
    cursor.executemany("INSERT INTO addresses (address_id, user_id, address_line, city, province, postal_code, is_default) VALUES (?, ?, ?, ?, ?, ?, ?)", addresses_data)
    
    # Data untuk tabel product_categories
    categories_data = [
        (1, 'Elektronik', 'Berbagai macam perangkat elektronik dari laptop hingga aksesoris.'),
        (2, 'Fashion', 'Pakaian pria dan wanita untuk segala musim.'),
        (3, 'Buku', 'Buku fiksi, non-fiksi, dan referensi.')
    ]
    cursor.executemany("INSERT INTO product_categories (category_id, name, description) VALUES (?, ?, ?)", categories_data)

    # Data untuk tabel products
    products_data = [
        (1, 'Laptop ProMax 14"', 'Kelebihan: Layar Retina Display, Chipset M3 Super Cepat, Baterai tahan 20 jam. Cocok untuk profesional kreatif.', 12000000, 15, 1, 'Garansi resmi 1 tahun. Klaim dapat dilakukan di service center resmi dengan membawa bukti pembelian.'),
        (2, 'Smartphone G-Pixel 9', 'Kelebihan: Kamera dengan AI terbaik, software update terjamin, desain minimalis.', 8500000, 30, 1, 'Garansi 2 tahun untuk cacat pabrik. Hubungi CS di 0800-1-12345 dengan menyertakan nomor pesanan.'),
        (3, 'Mouse Wireless SilentClick', 'Kelebihan: Tidak berisik (silent click), desain ergonomis, daya tahan baterai 6 bulan.', 250000, 100, 1, 'Garansi toko 1 bulan, tukar baru jika ada kerusakan.'),
        (4, 'T-Shirt Katun Basic', 'Kelebihan: Bahan katun combed 30s yang adem dan menyerap keringat. Jahitan rapi dan kuat.', 150000, 250, 2, 'Tidak ada garansi.'),
        (5, 'Buku "Sejarah Dunia"', 'Kelebihan: Ditulis oleh sejarawan terkemuka, dilengkapi ilustrasi berwarna, dan peta detail.', 95000, 80, 3, 'Garansi cetak, jika ada halaman yang hilang atau rusak bisa ditukar dengan buku baru.')
    ]
    cursor.executemany("INSERT INTO products (product_id, name, description, price, stock_quantity, category_id, warranty_info) VALUES (?, ?, ?, ?, ?, ?, ?)", products_data)

    # Data untuk tabel orders
    orders_data = [
        # Budi's Order (Laptop + Mouse), status: Delivered
        (1, 1, (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S'), 12250000, 'Delivered', 1, 'JNE-12345678'),
        # Citra's Order (T-Shirt), status: Shipped
        (2, 2, (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'), 300000, 'Shipped', 2, 'SICEPAT-98765432'),
        # Budi's 2nd Order (Buku), status: Processing
        (3, 1, (datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'), 95000, 'Paid', 3, None)
    ]
    cursor.executemany("INSERT INTO orders (order_id, user_id, order_date, total_amount, status, shipping_address_id, tracking_number) VALUES (?, ?, ?, ?, ?, ?, ?)", orders_data)

    # Data untuk tabel order_items
    order_items_data = [
        (1, 1, 1, 1, 12000000), # Order 1, Laptop
        (2, 1, 3, 1, 250000),  # Order 1, Mouse
        (3, 2, 4, 2, 150000),  # Order 2, T-Shirt x2
        (4, 3, 5, 1, 95000)    # Order 3, Buku
    ]
    cursor.executemany("INSERT INTO order_items (order_item_id, order_id, product_id, quantity, price_per_unit) VALUES (?, ?, ?, ?, ?)", order_items_data)

    # Data untuk tabel order_tracking (untuk menjawab "Dimana pesanan saya?")
    order_tracking_data = [
        # Tracking untuk Order 1 (Delivered)
        (1, 1, 'Pesanan telah diterima dan sedang diproses.', 'Gudang Bandung', (datetime.now() - timedelta(days=10, hours=2)).strftime('%Y-%m-%d %H:%M:%S')),
        (2, 1, 'Paket diserahkan ke kurir.', 'Gudang Bandung', (datetime.now() - timedelta(days=9)).strftime('%Y-%m-%d %H:%M:%S')),
        (3, 1, 'Paket dalam perjalanan menuju kota tujuan.', 'Transit Center Jakarta', (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d %H:%M:%S')),
        (4, 1, 'Paket telah tiba dan diterima oleh Budi Santoso.', 'Alamat Tujuan', (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')),
        
        # Tracking untuk Order 2 (Shipped)
        (5, 2, 'Pesanan telah diterima dan sedang dikemas.', 'Gudang Jakarta', (datetime.now() - timedelta(days=2, hours=3)).strftime('%Y-%m-%d %H:%M:%S')),
        (6, 2, 'Paket diserahkan kepada kurir SiCepat.', 'Gudang Jakarta', (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')),
        (7, 2, 'Paket sedang dalam perjalanan menuju alamat Anda.', 'Sortation Center Jakarta', (datetime.now() - timedelta(hours=12)).strftime('%Y-%m-%d %H:%M:%S'))
    ]
    cursor.executemany("INSERT INTO order_tracking (tracking_id, order_id, status_update, location, updated_at) VALUES (?, ?, ?, ?, ?)", order_tracking_data)

    # --- SIMPAN PERUBAHAN & TUTUP KONEKSI ---
    conn.commit()
    print("Data dummy berhasil dimasukkan.")

except sqlite3.Error as e:
    print(f"Terjadi error pada database: {e}")

finally:
    if conn:
        conn.close()
        print("Koneksi database ditutup.")