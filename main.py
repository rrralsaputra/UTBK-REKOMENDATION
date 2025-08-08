import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from load import load_data
from func import klasifikasi_program, hitung_skor, tentukan_kategori, cari_program, get_rekomendasi
import numpy as np

# Load data
data = load_data()
if data is None:
    exit()

# Tambah kolom kategori
data['KATEGORI'] = data['PROGRAM STUDI'].apply(klasifikasi_program)

# ================= GUI =================
root = tk.Tk()
root.title("🎓 Sistem Rekomendasi Program Studi UTBK")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ===== TAB 1: Pencarian =====
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="🔍 Pencarian Program Studi")

frame_input = ttk.LabelFrame(tab1, text="Filter Pencarian", padding="10")
frame_input.pack(fill=tk.X, padx=10, pady=10)

ttk.Label(frame_input, text="Universitas:").grid(row=0, column=0, sticky=tk.W, pady=5)
combo_univ = ttk.Combobox(frame_input, state="readonly", width=40)
combo_univ['values'] = ["Semua Universitas"] + sorted(data['UNIVERSITAS'].unique().tolist())
combo_univ.set("Semua Universitas")
combo_univ.grid(row=0, column=1, pady=5, padx=(10, 0))

ttk.Label(frame_input, text="Program Studi:").grid(row=1, column=0, sticky=tk.W, pady=5)
combo_prodi = ttk.Combobox(frame_input, state="readonly", width=40)
combo_prodi['values'] = ["Semua Program Studi"] + sorted(data['PROGRAM STUDI'].unique().tolist())
combo_prodi.set("Semua Program Studi")
combo_prodi.grid(row=1, column=1, pady=5, padx=(10, 0))

def cari_program_gui():
    for item in tree_search.get_children():
        tree_search.delete(item)
    hasil = cari_program(data, combo_univ.get(), combo_prodi.get())
    for _, row in hasil.iterrows():
        tree_search.insert("", tk.END, values=(
            row['PROGRAM STUDI'], row['UNIVERSITAS'],
            f"{row['RATA-RATA']:.1f}", f"{row['DAYA TAMPUNG 2024']:.0f}",
            f"{row['KEKETATAN']:.1f}x"
        ))
    messagebox.showinfo("Hasil", f"Ditemukan {len(hasil)} program studi" if len(hasil) > 0 else "Tidak ditemukan")

ttk.Button(frame_input, text="🔍 Cari", command=cari_program_gui).grid(row=2, column=1, pady=10, sticky=tk.E)

frame_hasil = ttk.LabelFrame(tab1, text="Hasil Pencarian", padding="10")
frame_hasil.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = ("Program Studi", "Universitas", "Rata-rata", "Daya Tampung", "Keketatan")
tree_search = ttk.Treeview(frame_hasil, columns=columns, show='headings', height=15)
for col in columns:
    tree_search.heading(col, text=col)
    tree_search.column(col, width=120)
scrollbar_search = ttk.Scrollbar(frame_hasil, orient=tk.VERTICAL, command=tree_search.yview)
tree_search.configure(yscrollcommand=scrollbar_search.set)
tree_search.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_search.pack(side=tk.RIGHT, fill=tk.Y)

# ===== TAB 2: Skor UTBK =====
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="📊 Input Skor UTBK")

frame_skor = ttk.LabelFrame(tab2, text="Input Skor UTBK (150-900)", padding="10")
frame_skor.pack(fill=tk.X, padx=10, pady=10)

entry_skor = {}
subtes = {
    'PU': 'Penalaran Umum', 'PPU': 'Pemahaman dan Penulisan Umum', 
    'PBM': 'Pemahaman Bacaan dan Menulis', 'PK': 'Pengetahuan Kuantitatif',
    'LBI': 'Literasi Bahasa Indonesia', 'LBE': 'Literasi Bahasa Inggris', 'PM': 'Penalaran Matematika'
}

row = 0
for kode, nama in subtes.items():
    ttk.Label(frame_skor, text=f"{kode} ({nama}):").grid(row=row, column=0, sticky=tk.W, pady=5)
    entry = ttk.Entry(frame_skor, width=10)
    entry.grid(row=row, column=1, pady=5, padx=(10, 0), sticky=tk.W)
    entry_skor[kode] = entry
    row += 1

def get_rekomendasi_gui():
    try:
        skor = {k: float(entry_skor[k].get()) for k in subtes}
        skor_lp, skor_lb, skor_pu = hitung_skor(skor['PU'], skor['PPU'], skor['PBM'], skor['PK'], skor['LBI'], skor['LBE'], skor['PM'])
        kategori = tentukan_kategori(skor_lp, skor_lb, skor_pu)
        rata_rata = np.mean(list(skor.values()))
        rekomendasi = get_rekomendasi(data, rata_rata, kategori)
        tampilkan_rekomendasi(rekomendasi, rata_rata, kategori)
    except:
        messagebox.showerror("Error", "Mohon isi skor dengan benar")

def tampilkan_rekomendasi(rekomendasi, skor_user, kategori):
    text_rekomendasi.delete(1.0, tk.END)
    hasil = f"🎯 Hasil Rekomendasi\n{'='*60}\n"
    hasil += f"Skor rata-rata: {skor_user:.1f}\nKategori: {kategori}\nJumlah rekomendasi: {len(rekomendasi)}\n\n"
    for i, (_, row) in enumerate(rekomendasi.head(10).iterrows(), 1):
        hasil += f"{i}. {row['PROGRAM STUDI']} - {row['UNIVERSITAS']} ({row['PROBABILITAS_LULUS']:.1f}%)\n"
    text_rekomendasi.insert(1.0, hasil)

ttk.Button(frame_skor, text="🎯 Dapatkan Rekomendasi", command=get_rekomendasi_gui).grid(row=row, column=1, pady=10, sticky=tk.E)

frame_rec = ttk.LabelFrame(tab2, text="Rekomendasi Program Studi", padding="10")
frame_rec.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
text_rekomendasi = scrolledtext.ScrolledText(frame_rec, wrap=tk.WORD, height=15)
text_rekomendasi.pack(fill=tk.BOTH, expand=True)

# ===== TAB 3: Analisis =====
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="📈 Analisis Database")

def analisis_data():
    text_analisis.delete(1.0, tk.END)
    total_program = len(data)
    total_univ = data['UNIVERSITAS'].nunique()
    kategori_count = data['KATEGORI'].value_counts().to_dict()
    rata_rata_grade = data['RATA-RATA'].mean()
    paling_kompetitif = data.loc[data['KEKETATAN'].idxmin()]['PROGRAM STUDI']
    grade_tertinggi = data.loc[data['RATA-RATA'].idxmax()]['PROGRAM STUDI']
    analisis = f"📊 Analisis Database\n{'='*50}\n"
    analisis += f"Total Program Studi: {total_program}\nTotal Universitas: {total_univ}\n"
    analisis += f"Rata-rata Passing Grade: {rata_rata_grade:.1f}\n"
    analisis += f"Program Paling Kompetitif: {paling_kompetitif}\n"
    analisis += f"Passing Grade Tertinggi: {grade_tertinggi}\n\n"
    for kategori, jumlah in kategori_count.items():
        analisis += f"{kategori}: {jumlah} ({(jumlah/total_program)*100:.1f}%)\n"
    text_analisis.insert(1.0, analisis)

ttk.Button(tab3, text="📊 Jalankan Analisis", command=analisis_data).pack(pady=10)
text_analisis = scrolledtext.ScrolledText(tab3, wrap=tk.WORD, height=25)
text_analisis.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
