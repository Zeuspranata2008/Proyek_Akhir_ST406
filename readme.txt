====================================================================
        SISTEM ANALISIS BIG DATA STORYTELLING MOTOGP (1949-2022)
====================================================================

Nama : Naufal Abid Syaikha Daffa 'Ulhaq
NIM  : 25.11.6552

--------------------------------------------------------------------
1. DESKRIPSI SINGKAT PROYEK
--------------------------------------------------------------------
Proyek ini adalah program analisis big data berbasis Python yang 
berjalan secara otomatis penuh (Full Automatic - Non Interactive) 
untuk membedah sejarah kejuaraan dunia balap motor Grand Prix (MotoGP) 
dari tahun 1949 hingga 2022.

Menggunakan pendekatan Multi-Relational Data Science, program ini 
mengintegrasikan 6 dataset master dari Kaggle sekaligus untuk melihat 
trajektori kemenangan legenda balap, dominasi era mesin konstruktor, 
spesialisasi sirkuit, dan supremasi negara penghasil juara dunia.
Program dilengkapi dengan pembersih data (data cleaning) otomatis 
dan standarisasi kelas balapan premier menjadi label "MotoGP".

Program akan secara senyap (tanpa pop-up) menghasilkan:
- Laporan statistik eksekutif ke dalam file hasil_analisis.txt
- Visualisasi 1: Line Plot (Trajektori kemenangan per musim)
- Visualisasi 2: Stacked Bar Plot (Aliansi pabrikan mesin/konstruktor)
- Visualisasi 3: Bar Plot (Top 10 legenda dengan kemenangan terbanyak)
- Visualisasi 4: Heatmap (Matriks spesialisasi sirkuit legenda balap)

--------------------------------------------------------------------
2. PANDUAN SINGKAT (CARA MENJALANKAN PROGRAM)
--------------------------------------------------------------------
Langkah-langkah untuk menjalankan file main.py:

1. Persiapan Dataset:
   Pastikan 6 file CSV dataset master dari Kaggle berada di folder 
   yang sama (sejajar) dengan file main.py dan utils.py:
   - grand-prix-race-winners.csv
   - riders-finishing-positions.csv
   - riders-info.csv
   - constructure-world-championship.csv
   - same-nation-podium-lockouts.csv
   - grand-prix-events-held.csv

2. Persiapan Library:
   Pastikan Python sudah terinstal (atau gunakan WinPython Portable). 
   Buka terminal/CMD dan instal library yang dibutuhkan dengan perintah:
   pip install pandas numpy matplotlib seaborn

3. Eksekusi Program:
   Buka terminal/CMD di direktori tempat file main.py berada, lalu 
   ketikkan perintah berikut:
   python main.py

4. Alur Kerja Program:
   Program berjalan secara otomatis penuh tanpa meminta input manual 
   di terminal. Sistem akan langsung memroses kelas premier (MotoGP) 
   dan 5 legenda balap (Marc Marquez, Valentino Rossi, Giacomo Agostini, 
   Mick Doohan, dan Casey Stoner).

5. Hasil Output:
   Jika program selesai (PROYEK SELESAI!), silakan periksa folder proyek. 
   Anda akan melihat 1 file laporan (hasil_analisis.txt) dan 4 file 
   gambar grafik (.png) dengan resolusi tinggi yang berhasil dibuat 
   secara otomatis di latar belakang.