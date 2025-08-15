# Database Schema

This document outlines the structure of the database used in the project, including the tables and sample data.

## Tables

### 1. **users**

| Column Name    | Data Type | Description                     |
|----------------|-----------|---------------------------------|
| `user_id`      | INTEGER   | Primary Key, Auto Increment     |
| `full_name`    | TEXT      | User's Full Name                |
| `email`        | TEXT      | User's Email Address (Unique)   |
| `password_hash`| TEXT      | Hashed Password                 |
| `phone_number` | TEXT      | User's Phone Number             |
| `created_at`   | TIMESTAMP | Timestamp when user was created |

#### Sample Data:

| user_id | full_name     | email                | password_hash | phone_number   | created_at           |
|---------|---------------|----------------------|---------------|----------------|----------------------|
| 1       | Budi Santoso  | budi.s@example.com    | ef92b7...     | 081234567890   | 2025-08-15 04:44:29  |
| 2       | Citra Lestari | citra.l@example.com   | 78928f...     | 085678901234   | 2025-08-15 04:44:29  |
| 3       | Agus Wijaya   | agus.w@example.com    | 65e84b...     | 087811223344   | 2025-08-15 04:44:29  |

---

### 2. **addresses**

| Column Name       | Data Type | Description                            |
|-------------------|-----------|----------------------------------------|
| `address_id`      | INTEGER   | Primary Key, Auto Increment            |
| `user_id`         | INTEGER   | Foreign Key: References `users(user_id)` |
| `address_line`    | TEXT      | Street Address                         |
| `city`            | TEXT      | City                                   |
| `province`        | TEXT      | Province                               |
| `postal_code`     | TEXT      | Postal Code                            |
| `is_default`      | BOOLEAN   | Flag to mark default address (0 or 1)   |

#### Sample Data:

| address_id | user_id | address_line                                         | city          | province       | postal_code | is_default |
|------------|---------|------------------------------------------------------|---------------|----------------|-------------|------------|
| 1          | 1       | Jl. Merdeka No. 10, Kel. Cihampelas                   | Bandung       | Jawa Barat     | 40131       | 1          |
| 2          | 2       | Jl. Sudirman Kav. 5, Apartemen Sejahtera Lt. 15      | Jakarta Selatan | DKI Jakarta   | 12190       | 1          |
| 3          | 1       | Kantor PT. Maju Mundur, Jl. Gatot Subroto No. 12    | Bandung       | Jawa Barat     | 40266       | 0          |

---

### 3. **product_categories**

| Column Name   | Data Type | Description                      |
|---------------|-----------|----------------------------------|
| `category_id` | INTEGER   | Primary Key, Auto Increment      |
| `name`        | TEXT      | Category Name (Unique)           |
| `description` | TEXT      | Category Description             |

#### Sample Data:

| category_id | name        | description                                                   |
|-------------|-------------|---------------------------------------------------------------|
| 1           | Elektronik  | Berbagai macam perangkat elektronik dari laptop hingga aksesoris. |
| 2           | Fashion     | Pakaian pria dan wanita untuk segala musim.                   |
| 3           | Buku        | Buku fiksi, non-fiksi, dan referensi.                         |

---

### 4. **products**

| Column Name    | Data Type | Description                             |
|----------------|-----------|-----------------------------------------|
| `product_id`   | INTEGER   | Primary Key, Auto Increment             |
| `name`         | TEXT      | Product Name                            |
| `description`  | TEXT      | Product Description                     |
| `price`        | REAL      | Price of the Product                    |
| `stock_quantity`| INTEGER  | Quantity of stock available             |
| `category_id`  | INTEGER   | Foreign Key: References `product_categories(category_id)` |
| `warranty_info`| TEXT      | Warranty Information                    |
| `created_at`   | TIMESTAMP | Timestamp when product was created      |

#### Sample Data:

| product_id | name                      | description                                                            | price    | stock_quantity | category_id | warranty_info                                           | created_at           |
|------------|---------------------------|------------------------------------------------------------------------|----------|----------------|-------------|---------------------------------------------------------|----------------------|
| 1          | Laptop ProMax 14"          | Kelebihan: Layar Retina Display, Chipset M3 Super Cepat, Baterai tahan 20 jam. | 12000000 | 15             | 1           | Garansi resmi 1 tahun. Klaim dapat dilakukan di service center resmi dengan membawa bukti pembelian. | 2025-08-15 04:44:29  |
| 2          | Smartphone G-Pixel 9       | Kelebihan: Kamera dengan AI terbaik, software update terjamin, desain minimalis. | 8500000  | 30             | 1           | Garansi 2 tahun untuk cacat pabrik. Hubungi CS di 0800-1-12345 dengan menyertakan nomor pesanan. | 2025-08-15 04:44:29  |
| 3          | Mouse Wireless SilentClick | Kelebihan: Tidak berisik (silent click), desain ergonomis, daya tahan baterai 6 bulan. | 250000   | 100            | 1           | Garansi toko 1 bulan, tukar baru jika ada kerusakan.  | 2025-08-15 04:44:29  |

---

### 5. **orders**

| Column Name         | Data Type | Description                        |
|---------------------|-----------|------------------------------------|
| `order_id`          | INTEGER   | Primary Key, Auto Increment        |
| `user_id`           | INTEGER   | Foreign Key: References `users(user_id)` |
| `order_date`        | TIMESTAMP | Date when the order was placed    |
| `total_amount`      | REAL      | Total amount of the order         |
| `status`            | TEXT      | Order status (pending, shipped, delivered, etc.) |
| `shipping_address_id`| INTEGER  | Foreign Key: References `addresses(address_id)` |
| `tracking_number`   | TEXT      | Tracking number for shipment      |

#### Sample Data:

| order_id | user_id | order_date           | total_amount | status    | shipping_address_id | tracking_number  |
|----------|---------|----------------------|--------------|-----------|---------------------|------------------|
| 1        | 1       | 2025-08-05 11:44:29  | 12250000.0   | Delivered | 1                   | JNE-12345678     |
| 2        | 2       | 2025-08-13 11:44:29  | 300000.0     | Shipped   | 2                   | SICEPAT-98765432 |
| 3        | 1       | 2025-08-15 06:44:29  | 95000.0      | Paid      | 3                   | NULL             |

---

### 6. **order_items**

| Column Name      | Data Type | Description                                |
|------------------|-----------|--------------------------------------------|
| `order_item_id`  | INTEGER   | Primary Key, Auto Increment                |
| `order_id`       | INTEGER   | Foreign Key: References `orders(order_id)` |
| `product_id`     | INTEGER   | Foreign Key: References `products(product_id)` |
| `quantity`       | INTEGER   | Quantity of the product in the order      |
| `price_per_unit` | REAL      | Price per unit of the product              |

#### Sample Data:

| order_item_id | order_id | product_id | quantity | price_per_unit |
|---------------|----------|------------|----------|----------------|
| 1             | 1        | 1          | 1        | 12000000.0     |
| 2             | 1        | 3          | 1        | 250000.0       |
| 3             | 2        | 4          | 2        | 150000.0       |
| 4             | 3        | 5          | 1        | 95000.0        |

---

### 7. **order_tracking**

| Column Name    | Data Type | Description                             |
|----------------|-----------|-----------------------------------------|
| `tracking_id`  | INTEGER   | Primary Key, Auto Increment             |
| `order_id`     | INTEGER   | Foreign Key: References `orders(order_id)` |
| `status_update`| TEXT      | Status update description               |
| `location`     | TEXT      | Location of the shipment               |
| `updated_at`   | TIMESTAMP | Timestamp of the tracking update       |
| `notes`        | TEXT      | Additional notes                        |

#### Sample Data:

| tracking_id | order_id | status_update                                             | location                | updated_at           | notes |
|-------------|----------|-----------------------------------------------------------|-------------------------|----------------------|-------|
| 1           | 1        | Pesanan telah diterima dan sedang diproses.               | Gudang Bandung          | 2025-08-05 09:44:29  | NULL  |
| 2           | 1        | Paket diserahkan ke kurir.                                | Gudang Bandung          | 2025-08-06 11:44:29  | NULL  |
| 3           | 1        | Paket dalam perjalanan menuju kota tujuan.               | Transit Center Jakarta  | 2025-08-07 11:44:29  | NULL  |
| 4           | 1        | Paket telah tiba dan diterima oleh Budi Santoso.          | Alamat Tujuan           | 2025-08-08 11:44:29  | NULL  |
| 5           | 2        | Pesanan telah diterima dan sedang dikemas.                | Gudang Jakarta          | 2025-08-13 08:44:29  | NULL  |

---

### 8. **sqlite_sequence**

| name             | seq |
|------------------|-----|
| users            | 3   |
| addresses        | 3   |
| product_categories| 3   |
| products         | 5   |
| orders           | 3   |
| order_items      | 4   |
| order_tracking   | 7   |
