import cv2
# Pastikan opencv-contrib-python terinstal: pip install opencv-contrib-python
# (Hapus opencv-python jika ada sebelumnya)
img = cv2.imread('dokumen_pudar.png', cv2.IMREAD_GRAYSCALE)
window_size = 25 # Harus ganjil
k_niblack = -0.2 # Nilai k untuk Niblack di OpenCV biasanya negatif
# Perhatikan urutan parameter: src, maxValue, type, blockSize, k, binarizationMethod
binary_niblack_cv = cv2.ximgproc.niBlackThreshold(img, 255, cv2.THRESH_BINARY,
                                                 window_size, k_niblack,
                                                 binarizationMethod=cv2.ximgproc.BINARIZATION_NIBLACK)
# cv2.imshow('Hasil Niblack OpenCV', binary_niblack_cv)
# cv2.waitKey(0)
# cv2.destroyAllWindows()