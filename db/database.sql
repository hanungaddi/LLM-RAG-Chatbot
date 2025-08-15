PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            phone_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
INSERT INTO users VALUES(1,'Budi Santoso','budi.s@example.com','ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f','081234567890','2025-08-15 04:44:29');
INSERT INTO users VALUES(2,'Citra Lestari','citra.l@example.com','78928f67cca5cbd6e66e0b3944ccbdc3242717ba038ba773a46c3945fa542ddf','085678901234','2025-08-15 04:44:29');
INSERT INTO users VALUES(3,'Agus Wijaya','agus.w@example.com','65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5','087811223344','2025-08-15 04:44:29');
CREATE TABLE addresses (
            address_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            address_line TEXT NOT NULL,
            city TEXT NOT NULL,
            province TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            is_default BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
INSERT INTO addresses VALUES(1,1,'Jl. Merdeka No. 10, Kel. Cihampelas','Bandung','Jawa Barat','40131',1);
INSERT INTO addresses VALUES(2,2,'Jl. Sudirman Kav. 5, Apartemen Sejahtera Lt. 15','Jakarta Selatan','DKI Jakarta','12190',1);
INSERT INTO addresses VALUES(3,1,'Kantor PT. Maju Mundur, Jl. Gatot Subroto No. 12','Bandung','Jawa Barat','40266',0);
CREATE TABLE product_categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        );
INSERT INTO product_categories VALUES(1,'Elektronik','Berbagai macam perangkat elektronik dari laptop hingga aksesoris.');
INSERT INTO product_categories VALUES(2,'Fashion','Pakaian pria dan wanita untuk segala musim.');
INSERT INTO product_categories VALUES(3,'Buku','Buku fiksi, non-fiksi, dan referensi.');
CREATE TABLE products (
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
INSERT INTO products VALUES(1,'Laptop ProMax 14"','Kelebihan: Layar Retina Display, Chipset M3 Super Cepat, Baterai tahan 20 jam. Cocok untuk profesional kreatif.',12000000.0,15,1,'Garansi resmi 1 tahun. Klaim dapat dilakukan di service center resmi dengan membawa bukti pembelian.','2025-08-15 04:44:29');
INSERT INTO products VALUES(2,'Smartphone G-Pixel 9','Kelebihan: Kamera dengan AI terbaik, software update terjamin, desain minimalis.',8500000.0,30,1,'Garansi 2 tahun untuk cacat pabrik. Hubungi CS di 0800-1-12345 dengan menyertakan nomor pesanan.','2025-08-15 04:44:29');
INSERT INTO products VALUES(3,'Mouse Wireless SilentClick','Kelebihan: Tidak berisik (silent click), desain ergonomis, daya tahan baterai 6 bulan.',250000.0,100,1,'Garansi toko 1 bulan, tukar baru jika ada kerusakan.','2025-08-15 04:44:29');
INSERT INTO products VALUES(4,'T-Shirt Katun Basic','Kelebihan: Bahan katun combed 30s yang adem dan menyerap keringat. Jahitan rapi dan kuat.',150000.0,250,2,'Tidak ada garansi.','2025-08-15 04:44:29');
INSERT INTO products VALUES(5,'Buku "Sejarah Dunia"','Kelebihan: Ditulis oleh sejarawan terkemuka, dilengkapi ilustrasi berwarna, dan peta detail.',95000.0,80,3,'Garansi cetak, jika ada halaman yang hilang atau rusak bisa ditukar dengan buku baru.','2025-08-15 04:44:29');
CREATE TABLE orders (
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
INSERT INTO orders VALUES(1,1,'2025-08-05 11:44:29',12250000.0,'Delivered',1,'JNE-12345678');
INSERT INTO orders VALUES(2,2,'2025-08-13 11:44:29',300000.0,'Shipped',2,'SICEPAT-98765432');
INSERT INTO orders VALUES(3,1,'2025-08-15 06:44:29',95000.0,'Paid',3,NULL);
CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
INSERT INTO order_items VALUES(1,1,1,1,12000000.0);
INSERT INTO order_items VALUES(2,1,3,1,250000.0);
INSERT INTO order_items VALUES(3,2,4,2,150000.0);
INSERT INTO order_items VALUES(4,3,5,1,95000.0);
CREATE TABLE order_tracking (
            tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            status_update TEXT NOT NULL,
            location TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        );
INSERT INTO order_tracking VALUES(1,1,'Pesanan telah diterima dan sedang diproses.','Gudang Bandung','2025-08-05 09:44:29',NULL);
INSERT INTO order_tracking VALUES(2,1,'Paket diserahkan ke kurir.','Gudang Bandung','2025-08-06 11:44:29',NULL);
INSERT INTO order_tracking VALUES(3,1,'Paket dalam perjalanan menuju kota tujuan.','Transit Center Jakarta','2025-08-07 11:44:29',NULL);
INSERT INTO order_tracking VALUES(4,1,'Paket telah tiba dan diterima oleh Budi Santoso.','Alamat Tujuan','2025-08-08 11:44:29',NULL);
INSERT INTO order_tracking VALUES(5,2,'Pesanan telah diterima dan sedang dikemas.','Gudang Jakarta','2025-08-13 08:44:29',NULL);
INSERT INTO order_tracking VALUES(6,2,'Paket diserahkan kepada kurir SiCepat.','Gudang Jakarta','2025-08-14 11:44:29',NULL);
INSERT INTO order_tracking VALUES(7,2,'Paket sedang dalam perjalanan menuju alamat Anda.','Sortation Center Jakarta','2025-08-14 23:44:29',NULL);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('users',3);
INSERT INTO sqlite_sequence VALUES('addresses',3);
INSERT INTO sqlite_sequence VALUES('product_categories',3);
INSERT INTO sqlite_sequence VALUES('products',5);
INSERT INTO sqlite_sequence VALUES('orders',3);
INSERT INTO sqlite_sequence VALUES('order_items',4);
INSERT INTO sqlite_sequence VALUES('order_tracking',7);
COMMIT;
