import numpy as np

def klasifikasi_program(program_name):
    """Mengklasifikasikan program studi ke SAINTEK/SOSHUM"""
    program = str(program_name).upper()
    saintek = ['TEKNIK', 'KEDOKTERAN', 'FARMASI', 'FISIKA', 'KIMIA', 'BIOLOGI', 'MATEMATIKA', 'INFORMATIKA', 'KOMPUTER']
    soshum = ['MANAJEMEN', 'EKONOMI', 'HUKUM', 'PSIKOLOGI', 'KOMUNIKASI', 'POLITIK', 'SOSIAL', 'SASTRA', 'BAHASA']

    for kata in saintek:
        if kata in program:
            return 'SAINTEK'
    for kata in soshum:
        if kata in program:
            return 'SOSHUM'
    return 'CAMPURAN'

def hitung_skor(pu, ppu, pbm, pk, lbi, lbe, pm):
    skor_lp = (lbi + lbe) / 2
    skor_lb = (pu + ppu + pbm) / 3
    skor_pu = (pk + pm) / 2
    return skor_lp, skor_lb, skor_pu

def tentukan_kategori(skor_lp, skor_lb, skor_pu):
    return 'SAINTEK' if skor_pu > max(skor_lb, skor_lp) else 'SOSHUM'

def cari_program(df, universitas=None, program_studi=None):
    hasil = df.copy()
    if universitas and universitas != "Semua Universitas":
        hasil = hasil[hasil['UNIVERSITAS'] == universitas]
    if program_studi and program_studi != "Semua Program Studi":
        hasil = hasil[hasil['PROGRAM STUDI'] == program_studi]
    return hasil.sort_values('RATA-RATA', ascending=False)

def get_rekomendasi(df, skor_user, kategori_user):
    if kategori_user in ['SAINTEK', 'SOSHUM']:
        filtered_df = df[df['KATEGORI'] == kategori_user].copy()
    else:
        filtered_df = df.copy()

    filtered_df['PROBABILITAS_LULUS'] = np.minimum(
        (skor_user / filtered_df['RATA-RATA']) * 100, 100
    ).round(1)

    rekomendasi = filtered_df[filtered_df['PROBABILITAS_LULUS'] >= 60].copy()
    if len(rekomendasi) == 0:
        filtered_df['selisih'] = abs(filtered_df['RATA-RATA'] - skor_user)
        rekomendasi = filtered_df.nsmallest(10, 'selisih')

    return rekomendasi.sort_values('PROBABILITAS_LULUS', ascending=False)
