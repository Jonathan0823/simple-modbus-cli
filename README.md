# Simple Modbus CLI Tool

Alat ringan untuk membaca/menulis holding register Modbus TCP lewat input terminal. Cocok untuk pengujian cepat tanpa dashboard Streamlit.

## Struktur Proyek
```
simple_modbus_cli/
├── main.py            # Script interaktif
├── requirements.txt   # Dependensi (pymodbus)
└── README.md          # Dokumentasi
```

## Cara Pakai
1. (Opsional) Buat virtualenv baru.
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   python main.py
   ```
4. Ikuti prompt:
   - Masukkan IP perangkat (default `127.0.0.1`).
   - Masukkan port (default `502`).
   - Masukkan Slave ID (default `1`).
   - Pilih aksi `r` (read) atau `w` (write), lalu isi alamat register & nilai.
   - Ketik `q` untuk keluar dan menutup koneksi.

## Catatan
- Script memakai `read_holding_registers` dan `write_register`, jadi pastikan perangkat mendukung holding register pada alamat yang Anda masukkan.
- Timeout koneksi diset ke 3 detik; sesuaikan di `main.py` jika jaringan Anda lambat.
- Jika terjadi error, pesan di terminal akan menunjukkan apakah masalah koneksi, penulisan, atau respon dari perangkat.
