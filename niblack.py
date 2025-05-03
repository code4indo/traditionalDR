import cv2
import numpy as np
import os
import argparse

def process_image_niblack(input_path, output_path, window_size, k_niblack):
    """Membaca gambar, menerapkan Niblack, dan menyimpan hasilnya."""
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Tidak dapat membaca citra: {input_path}")
        return False
    try:
        binary_niblack = cv2.ximgproc.niBlackThreshold(
            img, 255, cv2.THRESH_BINARY, window_size, k_niblack,
            binarizationMethod=cv2.ximgproc.BINARIZATION_NIBLACK)
        cv2.imwrite(output_path, binary_niblack)
        print(f"Berhasil memproses dan menyimpan: {output_path}")
        return True
    except Exception as e:
        print(f"Error saat memproses {input_path}: {e}")
        return False

def run_comparison_mode(input_dir, output_dir):
    print(f"Memulai mode perbandingan interaktif antara direktori:")
    print(f"  Input : {input_dir}")
    print(f"  Output: {output_dir}")
    print("\nNavigasi: Panah Kanan (Next), Panah Kiri (Back), 'q' atau Esc (Keluar)")

    if not os.path.isdir(input_dir):
        print(f"Error: Direktori input tidak ditemukan: {input_dir}")
        return
    if not os.path.isdir(output_dir):
        print(f"Error: Direktori output tidak ditemukan: {output_dir}")
        return

    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')
    image_pairs = []
    skipped_files = []

    for filename in sorted(os.listdir(input_dir)):
        if filename.lower().endswith(supported_extensions):
            original_path = os.path.join(input_dir, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_niblack{os.path.splitext(filename)[1]}"
            processed_path = os.path.join(output_dir, output_filename)
            if os.path.exists(processed_path):
                image_pairs.append((original_path, processed_path))
            else:
                skipped_files.append(filename)

    if not image_pairs:
        print("\nTidak ada pasangan gambar yang ditemukan untuk dibandingkan.")
        if skipped_files:
            print(f"File berikut dilewati karena tidak ada pasangannya di {output_dir}: {', '.join(skipped_files)}")
        return

    if skipped_files:
        print(f"\nWarning: File berikut dilewati karena tidak ada pasangannya di {output_dir}: {', '.join(skipped_files)}")

    current_index = 0
    window_name = "Perbandingan Gambar (Panah Kiri/Kanan, q/Esc untuk Keluar)"

    while True:
        original_path, processed_path = image_pairs[current_index]
        filename_display = os.path.basename(original_path)
        print(f"\nMenampilkan [{current_index + 1}/{len(image_pairs)}]: {filename_display}")

        try:
            img_original = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
            img_processed = cv2.imread(processed_path, cv2.IMREAD_GRAYSCALE)

            if img_original is None:
                print(f"  Error: Tidak dapat membaca gambar asli: {original_path}")
                comparison_display = np.zeros((200, 600), dtype=np.uint8)
                cv2.putText(comparison_display, f"Error loading original: {filename_display}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            elif img_processed is None:
                print(f"  Error: Tidak dapat membaca gambar hasil: {processed_path}")
                comparison_display = np.zeros((img_original.shape[0], img_original.shape[1]*2), dtype=np.uint8)
                cv2.putText(comparison_display, f"Error loading processed", (img_original.shape[1] + 10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                comparison_display[:, :img_original.shape[1]] = img_original
            else:
                h1, w1 = img_original.shape
                h2, w2 = img_processed.shape
                if h1 != h2:
                    if h1 > h2:
                        scale_percent = h2 / h1
                        new_width = int(w1 * scale_percent)
                        img_original_resized = cv2.resize(img_original, (new_width, h2), interpolation=cv2.INTER_AREA)
                        comparison_display = np.hstack((img_original_resized, img_processed))
                    else:
                        scale_percent = h1 / h2
                        new_width = int(w2 * scale_percent)
                        img_processed_resized = cv2.resize(img_processed, (new_width, h1), interpolation=cv2.INTER_AREA)
                        comparison_display = np.hstack((img_original, img_processed_resized))
                else:
                    comparison_display = np.hstack((img_original, img_processed))

            title_bar = np.zeros((30, comparison_display.shape[1]), dtype=np.uint8)
            cv2.putText(title_bar, f"Original: {filename_display} | Processed: {os.path.basename(processed_path)}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            final_display = np.vstack((title_bar, comparison_display))

            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow(window_name, final_display)

        except Exception as e:
            print(f"  Error saat memproses/menampilkan pasangan untuk {filename_display}: {e}")
            error_display = np.zeros((200, 600), dtype=np.uint8)
            cv2.putText(error_display, f"Error displaying pair: {filename_display}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
            cv2.imshow(window_name, error_display)

        print("Menunggu input tombol di jendela gambar (pastikan jendela aktif)...")
        key = -1
        while True:
            key = cv2.waitKey(100) & 0xFF
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                print("Jendela ditutup manual. Keluar dari mode perbandingan.")
                cv2.destroyAllWindows()
                return
            if key != 255:
                print(f"Kode tombol ditekan: {key}")
                break

        if key == ord('q') or key == 27:
            print("\nKeluar dari mode perbandingan.")
            break
        elif key == 83 or key == 67:
            print("Panah Kanan terdeteksi")
            current_index = min(current_index + 1, len(image_pairs) - 1)
        elif key == 81 or key == 68:
            print("Panah Kiri terdeteksi")
            current_index = max(current_index - 1, 0)
        elif key != 255:
            print(f"Tombol tidak dikenal ditekan: Kode = {key}")

    cv2.destroyAllWindows()

def run_processing_mode(input_dir, window_size, k_niblack):
    print("Memulai mode pemrosesan Niblack...")
    if not os.path.isdir(input_dir):
        print(f"Error: Direktori input tidak ditemukan: {input_dir}")
        return

    input_dir_norm = os.path.normpath(input_dir)
    input_base_name = os.path.basename(input_dir_norm)
    parent_dir = os.path.dirname(input_dir_norm)
    output_dir_name = f"{input_base_name}_niblack_output"
    output_dir = os.path.join(parent_dir if parent_dir else '.', output_dir_name)

    os.makedirs(output_dir, exist_ok=True)
    print(f"Direktori output (otomatis): {output_dir}")

    processed_count = 0
    error_count = 0
    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')

    print(f"Memulai pemrosesan gambar di: {input_dir}")
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_extensions):
            input_path = os.path.join(input_dir, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_niblack{os.path.splitext(filename)[1]}"
            output_path = os.path.join(output_dir, output_filename)

            if process_image_niblack(input_path, output_path, window_size, k_niblack):
                processed_count += 1
            else:
                error_count += 1
        else:
            print(f"Skipping non-image file: {filename}")

    print(f"\nPemrosesan selesai.")
    print(f"Total gambar diproses: {processed_count}")
    print(f"Total error: {error_count}")

def main():
    parser = argparse.ArgumentParser(description="Terapkan Niblack atau bandingkan hasil pada gambar dalam direktori.")
    parser.add_argument('--input_dir', type=str, required=True, help='Direktori berisi gambar input.')
    parser.add_argument('--output_dir', type=str, help='Direktori berisi gambar hasil (hanya digunakan dengan --compare).')
    parser.add_argument('--window_size', type=int, default=25, help='Ukuran window (ganjil) untuk Niblack (default: 25).')
    parser.add_argument('--k_niblack', type=float, default=-0.2, help='Nilai k untuk Niblack (default: -0.2).')
    parser.add_argument('--compare', action='store_true', help='Jalankan mode perbandingan (memerlukan --output_dir).')

    args = parser.parse_args()

    if args.compare:
        if not args.output_dir:
            parser.error("--output_dir diperlukan saat menggunakan --compare.")
        run_comparison_mode(args.input_dir, args.output_dir)
    else:
        if args.output_dir:
            print("Warning: --output_dir diabaikan karena tidak dalam mode --compare. Direktori output akan dibuat otomatis.")
        run_processing_mode(args.input_dir, args.window_size, args.k_niblack)

if __name__ == "__main__":
    main()