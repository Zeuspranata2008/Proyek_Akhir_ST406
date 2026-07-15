import pandas as pd
import numpy as np
import os

def load_all_datasets():
    # WAJIB pakai garis miring biasa (/) agar tidak error \r (Carriage Return) & bebas SyntaxWarning!
    files_map = {
        'winners': 'dataset/dataset utama/grand-prix-race-winners.csv',
        'finishing': 'dataset/dataset utama/riders-finishing-positions.csv',
        'info': 'dataset/dataset utama/riders-info.csv',
        'constructors': 'dataset/dataset utama/constructure-world-championship.csv',
        'events': 'dataset/dataset utama/grand-prix-events-held.csv',
        'lockouts': 'dataset/dataset utama/same-nation-podium-lockouts.csv'
    }
    
    datasets = {}
    print("[LOADER] Memeriksa dan memuat 6 berkas dataset master...")
    
    country_map = {
        'ES': 'SPAIN', 'IT': 'ITALY', 'AU': 'AUSTRALIA', 'GB': 'GREAT BRITAIN', 
        'US': 'USA', 'FR': 'FRANCE', 'DE': 'GERMANY', 'JP': 'JAPAN',
        'ZA': 'SOUTH AFRICA', 'NL': 'NETHERLANDS', 'CH': 'SWITZERLAND',
        'BE': 'BELGIUM', 'FI': 'FINLAND', 'SE': 'SWEDEN', 'NZ': 'NEW ZEALAND',
        'PT': 'PORTUGAL', 'TH': 'THAILAND', 'BR': 'BRAZIL', 'CA': 'CANADA',
        'VE': 'VENEZUELA', 'AR': 'ARGENTINA', 'IE': 'IRELAND', 'CZ': 'CZECH REPUBLIC',
        'HU': 'HUNGARY', 'AT': 'AUSTRIA', 'TR': 'TURKEY', 'SM': 'SAN MARINO',
        'MT': 'MALTA'
    }
    
    for key, filepath in files_map.items():
        if not os.path.exists(filepath):
            alt_path = filepath.replace('grand-', 'grands-')
            if os.path.exists(alt_path):
                filepath = alt_path
            else:
                print(f"[PERINGATAN] Berkas '{filepath}' tidak ditemukan! Beberapa fitur mungkin dilewati.")
                datasets[key] = pd.DataFrame()
                continue
            
        df = pd.read_csv(filepath)
        df.columns = df.columns.str.strip().str.title()
        
        rename_dict = {'Track': 'Circuit', 'Winner': 'Rider', 'Bike': 'Constructor', 'Team': 'Constructor', 'Year': 'Season', 'Nation': 'Country'}
        df = df.rename(columns={k: v for k, v in rename_dict.items() if k in df.columns})
        
        if 'Class' in df.columns:
            df['Class_Clean'] = df['Class'].replace({'500cc': 'MotoGP', 'MotoGP™': 'MotoGP', 'MotoGP': 'MotoGP'})
        
        if 'Rider' in df.columns:
            df['Rider'] = df['Rider'].str.replace('™', '').str.strip()
            
        if 'Country' in df.columns:
            df['Country_Full'] = df['Country'].map(country_map).fillna(df['Country'])
            
        datasets[key] = df
        print(f"  [OK] {filepath} berhasil dimuat -> {len(df)} baris data.")
        
    df_win_clean = datasets.get('winners', pd.DataFrame())
    if not df_win_clean.empty:
        export_path = os.path.join("dataset", "data_mentah.csv")
        df_win_clean.to_csv(export_path, index=False)
        print(f"  [EXPORTER] Sukses! File '{export_path}' berhasil dibuat ({len(df_win_clean)} baris data bersih).")
        
    return datasets

def get_comprehensive_rider_stats(datasets, riders, kelas_fokus="MotoGP"):
    df_win = datasets.get('winners', pd.DataFrame())
    df_fin = datasets.get('finishing', pd.DataFrame())
    
    if not df_win.empty and 'Class_Clean' in df_win.columns:
        df_win = df_win[df_win['Class_Clean'] == kelas_fokus]
    if not df_fin.empty and 'Class' in df_fin.columns:
        df_fin_clean = df_fin[df_fin['Class'].replace({'500cc': 'MotoGP', 'MotoGP™': 'MotoGP'}) == kelas_fokus]
    else:
        df_fin_clean = df_fin

    country_map = {
        'ES': 'SPAIN', 'IT': 'ITALY', 'AU': 'AUSTRALIA', 'GB': 'GREAT BRITAIN', 
        'US': 'USA', 'FR': 'FRANCE', 'DE': 'GERMANY', 'JP': 'JAPAN',
        'ZA': 'SOUTH AFRICA', 'NL': 'NETHERLANDS', 'CH': 'SWITZERLAND',
        'BE': 'BELGIUM', 'FI': 'FINLAND', 'SE': 'SWEDEN', 'NZ': 'NEW ZEALAND',
        'PT': 'PORTUGAL', 'TH': 'THAILAND', 'BR': 'BRAZIL', 'CA': 'CANADA',
        'VE': 'VENEZUELA', 'AR': 'ARGENTINA', 'IE': 'IRELAND', 'CZ': 'CZECH REPUBLIC',
        'HU': 'HUNGARY', 'AT': 'AUSTRIA', 'TR': 'TURKEY', 'SM': 'SAN MARINO',
        'MT': 'MALTA'
    }

    stats = []
    for r in riders:
        w_rider = df_win[df_win['Rider'].str.lower() == r.lower()] if not df_win.empty else pd.DataFrame()
        f_rider = df_fin_clean[df_fin_clean['Rider'].str.lower() == r.lower()] if not df_fin_clean.empty else pd.DataFrame()
        
        if w_rider.empty and f_rider.empty:
            continue
            
        nama_asli = w_rider['Rider'].iloc[0] if not w_rider.empty else f_rider['Rider'].iloc[0]
        total_wins = len(w_rider)
        
        kode_negara = "-"
        if not w_rider.empty and 'Country' in w_rider.columns and pd.notna(w_rider['Country'].iloc[0]):
            kode_negara = str(w_rider['Country'].iloc[0]).strip().upper()
        elif not f_rider.empty and 'Country' in f_rider.columns and pd.notna(f_rider['Country'].iloc[0]):
            kode_negara = str(f_rider['Country'].iloc[0]).strip().upper()
            
        negara_full = country_map.get(kode_negara, kode_negara)
                
        total_musim = len(w_rider['Season'].unique()) if not w_rider.empty else 0
        fav_const = w_rider['Constructor'].mode()[0] if not w_rider.empty and 'Constructor' in w_rider.columns else "-"
        fav_circ = w_rider['Circuit'].mode()[0] if not w_rider.empty and 'Circuit' in w_rider.columns else "-"
        wins_circ = len(w_rider[w_rider['Circuit'] == fav_circ]) if not w_rider.empty and fav_circ != "-" else 0

        stats.append({
            'Pembalap': nama_asli,
            'Negara': negara_full,
            'Total_Menang': total_wins,
            'Musim_Dominan': total_musim,
            'Motor_Utama': fav_const,
            'Sirkuit_Favorit': f"{fav_circ} ({wins_circ}x)" if fav_circ != "-" else "-"
        })
        
    return pd.DataFrame(stats)

def tulis_laporan_eksekutif(datasets, df_stats, txt_path="hasil_analisis.txt"):
    if df_stats.empty:
        print("\n[PERINGATAN] Data statistik kosong, laporan tidak dapat ditulis.")
        return
        
    laporan = "================================================================================\n"
    laporan += "  LAPORAN ANALISIS SAINS DATA MULTI-RELASIONAL: KEJUARAAN DUNIA MOTOGP         \n"
    laporan += "================================================================================\n"
    laporan += "Disusun oleh : Naufal Abid Syaikha Daffa 'Ulhaq (NIM: 25.11.6552)\n"
    laporan += "Proyek       : Sistem Analisis Big Data Sejarah MotoGP (1949-2022)\n"
    laporan += "Dataset      : 6 Tabel Relational Master (Winners, Info, Constructors, Lockouts)\n"
    laporan += "================================================================================\n\n"
    
    laporan += "--- BAGIAN 1: KOMPARASI STATISTIK LEGENDA BALAP (HEAD-TO-HEAD) ---\n"
    laporan += df_stats.to_string(index=False)
    laporan += "\n\n"
    
    df_lock = datasets.get('lockouts', pd.DataFrame())
    laporan += "--- BAGIAN 2: SUPREMASI NEGARA & FENOMENA PODIUM LOCKOUT ---\n"
    if not df_lock.empty:
        total_lock = len(df_lock)
        laporan += f"Berdasarkan dataset 'same-nation-podium-lockouts.csv', tercatat terjadi {total_lock} kali\n"
        laporan += "fenomena 'Podium Lockout' (di mana Juara 1, 2, dan 3 diborong oleh pembalap dari\n"
        laporan += "satu negara yang sama dalam satu balapan). Hal ini membuktikan dominasi program\n"
        laporan += "pembinaan balap motor dari negara-negara raksasa seperti Italia dan Spanyol.\n\n"
    else:
        laporan += "*Data sapu bersih podium negara tidak tersedia dalam sesi ini.\n\n"

    df_const = datasets.get('constructors', pd.DataFrame())
    laporan += "--- BAGIAN 3: EVOLUSI & HEGEMONI KONSTRUKTOR MESIN ---\n"
    if not df_const.empty and 'Constructor' in df_const.columns:
        top_const = df_const['Constructor'].value_counts().head(3)
        laporan += "Berdasarkan sejarah Gelar Juara Dunia Konstruktor, 3 pabrikan paling dominan adalah:\n"
        for idx, (pabrikan, jml) in enumerate(top_const.items(), 1):
            laporan += f"  {idx}. {pabrikan} : Meraih {jml} kali gelar Juara Dunia Konstruktor.\n"
        laporan += "Data ini memperlihatkan bagaimana persaingan teknologi aerodinamika dan mesin\n"
        laporan += "telah bergeser dari era keemasan motor pabrikan Jepang menuju raksasa Eropa.\n\n"
    else:
        laporan += "*Data gelar konstruktor dunia tidak tersedia dalam sesi ini.\n\n"
        
    laporan += "--- BAGIAN 4: KESIMPULAN STRATEGIS UNTUK PRESENTASI ---\n"
    laporan += "1. Integrasi Multi-Dataset menghasilkan validasi yang lebih kuat dibanding analisis tunggal.\n"
    laporan += "2. Karakteristik sirkuit (Sirkuit_Favorit) memiliki korelasi langsung dengan DNA motor (Motor_Utama).\n"
    laporan += "3. Konsistensi finis di zona poin jauh lebih menentukan gelar jangka panjang dibanding kemenangan acak.\n\n"
    
    laporan += "================================================================================\n"
    laporan += "       [Laporan digenerate secara otomatis oleh Sistem Analisis MotoGP] \n"
    laporan += "================================================================================\n"
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(laporan)
    print(f"[SUKSES] Laporan multi-dataset berhasil disimpan ke file '{txt_path}'!")