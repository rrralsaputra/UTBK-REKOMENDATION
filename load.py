import pandas as pd
from tkinter import messagebox

def load_data(file_path="data.csv"):
    """Memuat data dari file CSV"""
    try:
        df = pd.read_csv(file_path, encoding='windows-1252', sep=';')
        df.columns = df.columns.str.strip()
        
        numeric_cols = ['KEKETATAN', 'DAYA TAMPUNG 2024', 'PEMINAT', 'RATA-RATA']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
        
        print(f"✅ Data berhasil dimuat: {len(df)} program studi")
        return df
    except:
        messagebox.showerror("Error", f"File '{file_path}' tidak ditemukan!")
        return None
