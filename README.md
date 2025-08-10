# UTBK Recommendation System (GUI Python)

# Deskripsi
Program ini adalah aplikasi berbasis GUI menggunakan Tkinter yang dirancang untuk membantu calon mahasiswa memilih program studi berdasarkan data UTBK.  
Aplikasi memuat data dari file CSV berisi daftar program studi di berbagai universitas, mengklasifikasikan setiap program studi ke dalam kategori SAINTEK atau SOSHUM, dan menyediakan fitur pencarian serta analisis sederhana.

# Fitur Utama
1. Memuat Data dari CSV
   - Membaca file data.csv yang berisi informasi program studi, universitas, daya tampung, keketatan, dan rata-rata skor.

2. Klasifikasi Program Studi
   - Secara otomatis mengklasifikasikan program studi ke dalam kategori:
     - SAINTEK (sains dan teknologi)
     - SOSHUM (sosial dan humaniora)
     - CAMPURAN (tidak masuk dua kategori di atas)

3. Pencarian Program Studi
   - Cari program studi berdasarkan universitas dan/atau nama program
   - Menampilkan hasil pencarian dengan detail daya tampung, keketatan, dan rata-rata skor.

4. Input Skor UTBK
   - Pengguna memasukkan nilai subtes UTBK (PU, PPU, PBM, PK, LBI, LBE, PM).
   - Sistem menentukan kategori terbaik (SAINTEK/SOSHUM).
   - Memberikan rekomendasi program studi yang sesuai dengan probabilitas kelulusan.

5. Analisis Statistik
   - Menampilkan jumlah total program studi & universitas.
   - Distribusi kategori program studi.
   - Program paling kompetitif (keketatan terendah).
   - Program dengan passing grade tertinggi.

---

# Teknologi yang Digunakan
- Python (pandas, numpy, tkinter)
- CSV Data Processing
- GUI dengan Tkinter
- Logika Untuk menentukan rekomendasi

# Struktur Folder
- Data.csv  (Dataset program studi)
- load.py   (Modul untuk memuat & memproses data)
- func.py   (Modul berisi fungsi pendukung (klasifikasi, perhitungan skor, dll))
- main.py   (File utama untuk menjalankan aplikasi GUI)

# Cara Menjalankan
Pastikan Python sudah terinstal di komputer 
Install dependensi yang dibutuhkan ( Tkinter,Pandas,Numpy)
Pastikan file data.csv ada di folder yang sama dengan file main.py.
Jalankan program main.py




