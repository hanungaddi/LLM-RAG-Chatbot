# AI Chatbot for Toko Online

Proyek ini adalah chatbot berbasis AI yang dirancang untuk toko online, dibangun menggunakan kombinasi **Streamlit** `FRONTEND`, **Flask** `BACKEND`, **SQLite** `DATABASE`, dan **Pydantic AI** `LLM Agentic Framework`

Berikut adalah demo 3 pertanyaan yang diajukan:
- Apa saja list produk yang tersedia?
- Apakah ada garansi untuk produk tersebut? Bagaimana cara klaim garansinya? (Menggunakan Konteks Produk dari Memory chat sebelumnnya)
- Saya sudah melakukan transaksi dengan atas nama budi, boleh minta tolong check bagaimaa kondisinya?

https://github.com/user-attachments/assets/57465f82-b2ec-4d06-a7b6-8bc4c219bded


## Struktur Proyek

```
/LLM-RAG-Chatbot/
├── .streamlit/
│   └── secrets.toml        # File untuk menyimpan kredensial sensitif
├── core/
│   ├── __init__.py         # Inisialisasi modul utama
│   ├── agent.py            # Logika chatbot, tidak berubah
│   └── ui.py               # UI yang dimodifikasi untuk memanggil API
├── db/
│   ├── populate_db.py      # Skrip untuk mengisi database
│   └── toko_online.db      # Database SQLite untuk chatbot
├── .env                    # Tempat menyimpan config (GROQ API KEY)
├── app.py                  # Frontend dengan Streamlit
├── backend.py              # Server REST API menggunakan Flask
└── requirements.txt        # File dependensi untuk proyek ini
```

## Database Design
Database dirancang untuk menyimpan data esensial dari sebuah toko online, termasuk pengguna, produk, dan transaksi. Skema ini memungkinkan agent AI untuk melakukan JOIN antar tabel untuk menjawab pertanyaan yang kompleks.
<img width="1019" height="735" alt="db_schema" src="https://github.com/user-attachments/assets/8d3750df-9a48-49b5-9d45-f117d836a710" />
Database ini terdiri dari 7 tabel utama, di antaranya:
- users: Menyimpan data pelanggan.
- addresses: Menyimpan alamat user.
- products: Katalog semua produk yang dijual.
- products_categories: Menyimpan data kategori produk.
- orders: Riwayat semua transaksi yang dilakukan.
- order_items: Detail produk di dalam setiap transaksi.
- order_tracking: Status pengiriman untuk setiap pesanan.

## Fitur

- **Chatbot AI**: Berbasis **agent.py**, memberikan jawaban otomatis berdasarkan data toko online.
- **UI Chatbot**: Antarmuka pengguna interaktif menggunakan **Streamlit**.
- **Backend API**: Menggunakan **Flask** untuk mengelola permintaan dan respons API.
- **Database**: Database SQLite untuk menyimpan informasi produk dan transaksi.

## Instalasi

1. **Clone repository ini**:

   ```bash
   git clone https://github.com/hanungaddi/LLM-RAG-Chatbot.git
   cd LLM-RAG-Chatbot
   ```

2. **Instal dependensi**:

   Pastikan Anda menggunakan virtual environment (venv) dan instal dependensi menggunakan `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

3. **Inisialisasi database**:

   Jalankan skrip `populate_db.py` untuk mengisi database dengan data produk dan informasi lainnya.

   ```bash
   python db/populate_db.py
   ```

   Dapat dilakukan pengecheckan database menggunakan database manager seperti `DBeaver`, dengan meng-koneksikan langsung file `db/toko_online.db`
4. **Menjalankan aplikasi**:

   - Untuk menjalankan backend API, gunakan Flask:

     ```bash
     python backend.py
     ```

   - Untuk menjalankan frontend dengan Streamlit, gunakan:

     ```bash
     streamlit run app.py
     ```

## Penggunaan

1. Akses frontend chatbot di `http://localhost:8501` setelah menjalankan `streamlit run app.py`.
2. Gunakan API Flask di `http://localhost:5000` untuk berinteraksi dengan chatbot secara langsung.

## Pengembangan

- **agent.py**: Tempat logika AI dan interaksi chatbot dikendalikan. Anda bisa mengeditnya untuk memperbarui kemampuan chatbot.
- **ui.py**: Digunakan untuk menghubungkan antarmuka Streamlit dengan backend API.
- **backend.py**: Backend API menggunakan Flask untuk menangani request dari antarmuka dan mengembalikan respons.
- **populate_db.py**: Skrip untuk mengisi database dengan data produk yang diperlukan oleh chatbot.

## Logic
Menggunakan sistem **Agentic**,
Terdapat 2 **Tool Calling** pada sistem RAG ini, 
- `get_database_schema` (**core/agent.py Line 36**) yang digunakan untuk mengambil context table yang tersedia didatabase.
- `run_sql_query` (**core/agent.py Line 51**) yang digunakan untuk running SQL Query yang telah digenerate LLM menggunakan context pertanyaan user dan schema yang telah diambil. (Metode ini biasanya diperlukan step tambahan seperti menggunakan similarity search dengan embedding untuk mengambil table yang relevan untuk mengurangi **token usage** dan irrelevant context. Karena database masih terbilang kecil, sehingga tidak diperlukan)

Setelah data diambil, LLM akan mencoba untuk generate jawaban dengan bahasa natural dengan context data yang diambil untuk menjawab pertanyaan dari user. Jika pertanyaan dapat dijawab tanpa perlu SQL, agent tidak akan melakukan tool calling.

## Dependensi

Daftar dependensi yang diperlukan untuk proyek ini:

- Flask `Backend`
- Streamlit `Frontend`
- SQLite `Database`
- Groq `Model Provider`
- dan lainnya (tercantum di `requirements.txt`)

Model LLM yang digunakan adalah `GPT OSS 20B`   
