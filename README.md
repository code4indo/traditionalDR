# Proyek CLAHE

Proyek ini bertujuan untuk menerapkan algoritma Contrast Limited Adaptive Histogram Equalization (CLAHE) pada citra menggunakan pustaka OpenCV di Python. CLAHE berguna untuk meningkatkan kontras citra, terutama pada citra dengan pencahayaan yang tidak seragam atau citra yang pudar, seperti dokumen lama.

## Tujuan

Meningkatkan kualitas visual citra dengan kontras rendah atau tidak merata melalui penerapan CLAHE.

## Instalasi

Proyek ini menggunakan [Poetry](https://python-poetry.org/) untuk manajemen dependensi.

1.  **Instal Poetry:** Jika Anda belum memilikinya, ikuti petunjuk instalasi di [situs web Poetry](https://python-poetry.org/docs/#installation).
2.  **Instal Dependensi:** Dari direktori root proyek, jalankan perintah berikut:
    ```bash
    poetry install
    ```

## Penggunaan

Skrip ini memiliki dua mode operasi utama: **Pemrosesan** (menerapkan CLAHE) dan **Perbandingan** (menampilkan gambar asli vs hasil).

### Mode Pemrosesan (Default)

Mode ini menerapkan algoritma CLAHE pada semua gambar di direktori input dan menyimpannya ke direktori output yang dibuat secara otomatis.

1.  **Siapkan Direktori Input:**
    *   Pastikan direktori input (`--input_dir`) berisi semua gambar yang ingin Anda proses.

2.  **Jalankan Skrip:**
    Gunakan perintah berikut, ganti `/path/ke/direktori/input` dengan path sebenarnya:

    ```bash
    # Menjalankan dengan parameter default
    poetry run python clahe.py --input_dir /path/ke/direktori/input 
    ```

    Anda juga dapat menyesuaikan parameter CLAHE:

    ```bash
    # Menjalankan dengan parameter kustom
    poetry run python clahe.py --input_dir /path/ke/direktori/input --clip_limit 3.0 --tile_grid_size 16 16
    ```

    *   `--input_dir`: (Wajib) Path ke direktori yang berisi gambar-gambar input.
    *   `--clip_limit`: (Opsional) Batas kontras untuk CLAHE. Default: `2.0`.
    *   `--tile_grid_size`: (Opsional) Ukuran grid tile (tinggi lebar) untuk CLAHE. Default: `8 8`.

    Direktori output akan dibuat secara otomatis di lokasi yang sama dengan direktori input, dengan nama `<nama_direktori_input>_clahe_output`. Hasil pemrosesan akan disimpan di dalamnya.

### Mode Perbandingan

Mode ini digunakan untuk menampilkan perbandingan berdampingan antara gambar asli (dari direktori input) dan gambar hasil CLAHE (dari direktori output). Mode ini berguna untuk mengevaluasi hasil pemrosesan secara visual.

1.  **Siapkan Direktori Input dan Output:**
    *   Pastikan direktori input (`--input_dir`) berisi gambar asli.
    *   Pastikan direktori output (`--output_dir`) berisi gambar hasil pemrosesan CLAHE (misalnya, direktori yang dibuat oleh mode pemrosesan). Nama file di direktori output diasumsikan mengikuti pola `<nama_asli>_clahe.<ekstensi>`.

2.  **Jalankan Skrip dengan Flag `--compare`:**
    Gunakan perintah berikut, ganti path placeholder:

    ```bash
    poetry run python clahe.py --compare --input_dir /path/ke/direktori/input --output_dir /path/ke/direktori/output_hasil
    ```

    *   `--compare`: (Wajib) Flag untuk mengaktifkan mode perbandingan.
    *   `--input_dir`: (Wajib) Path ke direktori yang berisi gambar asli.
    *   `--output_dir`: (Wajib) Path ke direktori yang berisi gambar hasil CLAHE.

    Skrip akan menampilkan jendela perbandingan untuk setiap pasangan gambar yang ditemukan. Tekan tombol apa saja pada keyboard untuk melanjutkan ke gambar berikutnya.

## Dependensi

*   Python (^3.9)
*   opencv-python
*   numpy

Dikelola dengan [Poetry](https://python-poetry.org/).
