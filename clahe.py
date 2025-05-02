import cv2
import numpy as np

# Baca citra sebagai grayscale
img = cv2.imread('dokumen_pudar_tidak_seragam.png', cv2.IMREAD_GRAYSCALE)
if img is None:
    print("Error: Citra tidak dapat dibaca.")
else:
    # Buat objek CLAHE
    # clipLimit: Batas kontras (default 40.0). Nilai lebih rendah mengurangi noise amplification.
    # tileGridSize: Ukuran grid tile (default (8, 8)). Ukuran lebih kecil meningkatkan lokalisasi.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    # Terapkan CLAHE
    cl1 = clahe.apply(img)

    # Tampilkan hasil (opsional)
    hasil_clahe = np.hstack((img, cl1)) # Gabungkan citra asli dan hasil
    cv2.imshow('Original vs CLAHE', hasil_clahe)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Simpan hasil (opsional)
    # cv2.imwrite('dokumen_clahe.png', cl1)