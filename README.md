
# Proyek CLAHE & Niblack


Proyek ini bertujuan untuk menerapkan dua teknik pemrosesan citra pada dokumen digital menggunakan pustaka OpenCV di Python:

- **CLAHE (Contrast Limited Adaptive Histogram Equalization):** Untuk meningkatkan kontras citra, terutama pada citra dengan pencahayaan yang tidak seragam atau citra yang pudar.
- **Niblack:** Untuk melakukan binarisasi lokal pada citra dokumen, sangat berguna untuk dokumen dengan latar belakang tidak seragam atau noise.

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

Terdapat dua skrip utama: `clahe.py` dan `niblack.py`. Keduanya mendukung dua mode operasi: **Pemrosesan** (batch processing) dan **Perbandingan** (side-by-side comparison).


### Mode Pemrosesan (Default)

#### CLAHE

Menerapkan algoritma CLAHE pada semua gambar di direktori input dan menyimpannya ke direktori output otomatis.

1. **Siapkan Direktori Input:**
    * Pastikan direktori input (`--input_dir`) berisi semua gambar yang ingin Anda proses.
2. **Jalankan Skrip:**

    ```bash
    # Menjalankan dengan parameter default
    poetry run python clahe.py --input_dir /path/ke/direktori/input
    ```

    Anda juga dapat menyesuaikan parameter CLAHE:

    ```bash
    poetry run python clahe.py --input_dir /path/ke/direktori/input --clip_limit 3.0 --tile_grid_size 16 16
    ```

    * `--input_dir`: (Wajib) Path ke direktori yang berisi gambar-gambar input.
    * `--clip_limit`: (Opsional) Batas kontras untuk CLAHE. Default: `2.0`.
    * `--tile_grid_size`: (Opsional) Ukuran grid tile (tinggi lebar) untuk CLAHE. Default: `8 8`.

    Direktori output akan dibuat otomatis dengan nama `<nama_direktori_input>_clahe_output`.

#### Niblack

Menerapkan algoritma Niblack pada semua gambar di direktori input dan menyimpannya ke direktori output otomatis.

1. **Siapkan Direktori Input:**
    * Pastikan direktori input (`--input_dir`) berisi semua gambar yang ingin Anda proses.
2. **Jalankan Skrip:**

    ```bash
    # Menjalankan dengan parameter default
    poetry run python niblack.py --input_dir /path/ke/direktori/input
    ```

    Anda juga dapat menyesuaikan parameter Niblack:

    ```bash
    poetry run python niblack.py --input_dir /path/ke/direktori/input --window_size 31 --k_niblack -0.1
    ```

    * `--input_dir`: (Wajib) Path ke direktori yang berisi gambar-gambar input.
    * `--window_size`: (Opsional) Ukuran window (ganjil) untuk Niblack. Default: `25`.
    * `--k_niblack`: (Opsional) Nilai k untuk Niblack. Default: `-0.2`.

    Direktori output akan dibuat otomatis dengan nama `<nama_direktori_input>_niblack_output`.


### Mode Perbandingan

Mode ini digunakan untuk menampilkan perbandingan berdampingan antara gambar asli (dari direktori input) dan gambar hasil pemrosesan (CLAHE atau Niblack) dari direktori output. Mode ini berguna untuk mengevaluasi hasil pemrosesan secara visual.

1. **Siapkan Direktori Input dan Output:**
    * Pastikan direktori input (`--input_dir`) berisi gambar asli.
    * Pastikan direktori output (`--output_dir`) berisi gambar hasil pemrosesan (misal, direktori yang dibuat oleh mode pemrosesan). Nama file di direktori output diasumsikan mengikuti pola `<nama_asli>_clahe.<ekstensi>` untuk CLAHE dan `<nama_asli>_niblack.<ekstensi>` untuk Niblack.
2. **Jalankan Skrip dengan Flag `--compare`:**

    Untuk CLAHE:
    ```bash
    poetry run python clahe.py --compare --input_dir /path/ke/direktori/input --output_dir /path/ke/direktori/output_hasil
    ```

    Untuk Niblack:
    ```bash
    poetry run python niblack.py --compare --input_dir /path/ke/direktori/input --output_dir /path/ke/direktori/output_hasil
    ```

    * `--compare`: (Wajib) Flag untuk mengaktifkan mode perbandingan.
    * `--input_dir`: (Wajib) Path ke direktori yang berisi gambar asli.
    * `--output_dir`: (Wajib) Path ke direktori yang berisi gambar hasil pemrosesan.

    Skrip akan menampilkan jendela perbandingan untuk setiap pasangan gambar yang ditemukan. Tekan tombol apa saja pada keyboard untuk melanjutkan ke gambar berikutnya.

## Dependensi

* Python (^3.9)
* opencv-contrib-python
* numpy

Dikelola dengan [Poetry](https://python-poetry.org/).
