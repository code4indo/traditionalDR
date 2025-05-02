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

1.  Pastikan Anda memiliki file citra input (misalnya, `dokumen_pudar_tidak_seragam.png`) di direktori yang sama dengan skrip `clahe.py`.
2.  Jalankan skrip Python:
    ```bash
    poetry run python clahe.py
    ```
    Skrip akan membaca citra, menerapkan CLAHE, dan menampilkan citra asli berdampingan dengan citra hasil pemrosesan. Tekan tombol apa saja untuk menutup jendela tampilan.

## Dependensi

*   Python (^3.9)
*   opencv-python
*   numpy

Dikelola dengan [Poetry](https://python-poetry.org/).
