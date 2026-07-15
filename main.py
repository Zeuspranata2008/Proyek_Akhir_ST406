import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from utils import load_all_datasets, get_comprehensive_rider_stats, tulis_laporan_eksekutif

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'

def main():
    print("=======================================================================")
    print(" SISTEM ANALISIS BIG DATA STORYTELLING MOTOGP (FULL OTOMATIS) ")
    print("=======================================================================\n")
    
    datasets = load_all_datasets()
    df_win = datasets.get('winners', pd.DataFrame())
    if df_win.empty:
        print("[ERROR FATAL] Dataset utama 'grand-prix-race-winners.csv' wajib ada!")
        return
        
    kelas_fokus = 'MotoGP'
    list_riders = ['Marc Marquez', 'Valentino Rossi', 'Giacomo Agostini', 'Mick Doohan', 'Casey Stoner']
    
    print(f"\nFokus Analisis   : Kelas [{kelas_fokus}]")
    print(f"Legenda Terpilih : {', '.join(list_riders)}\n")
    print("[PROSES] Sedang memproses dan menyimpan 4 grafik ke folder proyek \n")
    
    df_stats = get_comprehensive_rider_stats(datasets, list_riders, kelas_fokus)
    if df_stats.empty:
        print("[ERROR] Data pembalap tidak ditemukan di dalam dataset!")
        return
        
    riders_valid = df_stats['Pembalap'].tolist()
    df_story = df_win[(df_win['Class_Clean'] == kelas_fokus) & (df_win['Rider'].isin(riders_valid))].copy()

    plt.figure(figsize=(14, 6))
    df_trend = df_story.groupby(['Season', 'Rider']).size().reset_index(name='Wins')
    sns.lineplot(data=df_trend, x='Season', y='Wins', hue='Rider', marker='o', linewidth=2.5, markersize=8)
    plt.title(f'Grafik 1: Trajektori Kemenangan Grand Prix per Musim ({kelas_fokus})', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Musim Kejuaraan', fontsize=11)
    plt.ylabel('Jumlah Kemenangan', fontsize=11)
    plt.legend(title='Legenda Balap', loc='upper left', frameon=True)
    plt.tight_layout()
    plt.savefig("motogp_1_tren_musim.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  [1/4] Tersimpan: motogp_1_tren_musim.png")

    plt.figure(figsize=(12, 6))
    df_const = df_story.groupby(['Rider', 'Constructor']).size().unstack(fill_value=0)
    df_const.plot(kind='bar', stacked=True, colormap='Set1', figsize=(12, 6), edgecolor='black', linewidth=0.8)
    plt.title('Grafik 2: Aliansi Pabrikan Mesin & Kemenangan Legenda', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Pembalap', fontsize=11)
    plt.ylabel('Total Kemenangan Grand Prix', fontsize=11)
    plt.xticks(rotation=0, fontweight='bold')
    plt.legend(title='Konstruktor', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig("motogp_2_pabrikan.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  [2/4] Tersimpan: motogp_2_pabrikan.png")

    plt.figure(figsize=(12, 5))
    df_top10 = df_win[df_win['Class_Clean'] == kelas_fokus]['Rider'].value_counts().head(10)
    sns.barplot(x=df_top10.index, y=df_top10.values, hue=df_top10.index, palette="magma", legend=False)
    plt.title(f'Grafik 3: Top 10 Pembalap dengan Kemenangan Terbanyak Sepanjang Masa ({kelas_fokus})', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Nama Pembalap', fontsize=11)
    plt.ylabel('Total Kemenangan Grand Prix', fontsize=11)
    plt.xticks(rotation=20, ha='right', fontweight='bold')
    plt.tight_layout()
    plt.savefig("motogp_3_top10_alltime.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  [3/4] Tersimpan: motogp_3_top10_alltime.png")

    plt.figure(figsize=(12, 8))
    top_circuits = df_story['Circuit'].value_counts().head(10).index
    df_heat = df_story[df_story['Circuit'].isin(top_circuits)].groupby(['Circuit', 'Rider']).size().unstack(fill_value=0)
    
    sns.heatmap(df_heat, annot=True, fmt="d", cmap="YlGnBu", cbar=True, linewidths=.5)
    plt.title('Grafik 4: Matriks Spesialisasi Sirkuit (Siapa Raja di Trek Mana?)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Pembalap', fontsize=11)
    plt.ylabel('Nama Sirkuit Grand Prix', fontsize=11)
    plt.tight_layout()
    plt.savefig("motogp_4_sirkuit_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("  [4/4] Tersimpan: motogp_4_sirkuit_heatmap.png")

    print("\n[PROSES] Menyusun dan menyimpan laporan eksekutif...")
    tulis_laporan_eksekutif(datasets, df_stats, "hasil_analisis.txt")
    print("\n[PROYEK SELESAI] Seluruh 4 grafik .png dan laporan .txt sudah tersedia di folder proyek.")

if __name__ == "__main__":
    main()