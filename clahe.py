import cv2
import numpy as np
import os
import argparse

def process_image(input_path, output_path, clip_limit, tile_grid_size):
    """Membaca gambar, menerapkan CLAHE, dan menyimpan hasilnya."""
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Tidak dapat membaca citra: {input_path}")
        return False

    try:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        cl1 = clahe.apply(img)
        cv2.imwrite(output_path, cl1)
        print(f"Berhasil memproses dan menyimpan: {output_path}")
        return True
    except Exception as e:
        print(f"Error saat memproses {input_path}: {e}")
        return False

def run_comparison_mode(input_dir, output_dir):
    """Menjalankan mode perbandingan gambar dengan navigasi next/back."""
    print(f"Memulai mode perbandingan interaktif antara direktori:")
    print(f"  Input : {input_dir}")
    print(f"  Output: {output_dir}")
    print("\\nNavigasi: Panah Kanan (Next), Panah Kiri (Back), 'q' atau Esc (Keluar)")

    if not os.path.isdir(input_dir):
        print(f"Error: Direktori input tidak ditemukan: {input_dir}")
        return
    if not os.path.isdir(output_dir):
        print(f"Error: Direktori output tidak ditemukan: {output_dir}")
        return

    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')
    image_pairs = []
    skipped_files = []

    # 1. Kumpulkan semua pasangan gambar yang valid
    for filename in sorted(os.listdir(input_dir)):
        if filename.lower().endswith(supported_extensions):
            original_path = os.path.join(input_dir, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_clahe{os.path.splitext(filename)[1]}"
            processed_path = os.path.join(output_dir, output_filename)

            if os.path.exists(processed_path):
                image_pairs.append((original_path, processed_path))
            else:
                skipped_files.append(filename)
        else:
            # Abaikan file non-gambar
            pass

    if not image_pairs:
        print("\\nTidak ada pasangan gambar yang ditemukan untuk dibandingkan.")
        if skipped_files:
             print(f"File berikut dilewati karena tidak ada pasangannya di {output_dir}: {', '.join(skipped_files)}")
        return

    if skipped_files:
         print(f"\\nWarning: File berikut dilewati karena tidak ada pasangannya di {output_dir}: {', '.join(skipped_files)}")

    # 2. Loop Navigasi
    current_index = 0
    window_name = "Perbandingan Gambar (Panah Kiri/Kanan, q/Esc untuk Keluar)"

    while True:
        original_path, processed_path = image_pairs[current_index]
        filename_display = os.path.basename(original_path)
        print(f"\\nMenampilkan [{current_index + 1}/{len(image_pairs)}]: {filename_display}")

        try:
            img_original = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
            img_processed = cv2.imread(processed_path, cv2.IMREAD_GRAYSCALE)

            if img_original is None:
                print(f"  Error: Tidak dapat membaca gambar asli: {original_path}")
                comparison_display = np.zeros((200, 600), dtype=np.uint8) # Placeholder hitam
                cv2.putText(comparison_display, f"Error loading original: {filename_display}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            elif img_processed is None:
                print(f"  Error: Tidak dapat membaca gambar hasil: {processed_path}")
                comparison_display = np.zeros((img_original.shape[0], img_original.shape[1]*2), dtype=np.uint8) # Placeholder
                cv2.putText(comparison_display, f"Error loading processed", (img_original.shape[1] + 10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                comparison_display[:, :img_original.shape[1]] = img_original # Tampilkan yg asli jika ada
            else:
                # Tangani perbedaan ukuran (resize untuk display)
                h1, w1 = img_original.shape
                h2, w2 = img_processed.shape
                if h1 != h2:
                    # Resize gambar yang lebih tinggi agar sesuai dengan yang lebih pendek
                    if h1 > h2:
                        scale_percent = h2 / h1
                        new_width = int(w1 * scale_percent)
                        img_original_resized = cv2.resize(img_original, (new_width, h2), interpolation=cv2.INTER_AREA)
                        comparison_display = np.hstack((img_original_resized, img_processed))
                    else: # h2 > h1
                        scale_percent = h1 / h2
                        new_width = int(w2 * scale_percent)
                        img_processed_resized = cv2.resize(img_processed, (new_width, h1), interpolation=cv2.INTER_AREA)
                        comparison_display = np.hstack((img_original, img_processed_resized))
                else:
                    comparison_display = np.hstack((img_original, img_processed))


            # Tambahkan teks nama file di atas gambar
            title_bar = np.zeros((30, comparison_display.shape[1]), dtype=np.uint8)
            cv2.putText(title_bar, f"Original: {filename_display} | Processed: {os.path.basename(processed_path)}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            final_display = np.vstack((title_bar, comparison_display))

            # --- FULLSCREEN WINDOW ---
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow(window_name, final_display)

        except Exception as e:
            print(f"  Error saat memproses/menampilkan pasangan untuk {filename_display}: {e}")
            # Tampilkan pesan error di window jika memungkinkan
            error_display = np.zeros((200, 600), dtype=np.uint8)
            cv2.putText(error_display, f"Error displaying pair: {filename_display}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
            cv2.imshow(window_name, error_display)


        # 3. Tangkap input tombol
        print("Menunggu input tombol di jendela gambar (pastikan jendela aktif)...")
        key = -1
        while True:
            key = cv2.waitKey(100) & 0xFF  # Cek setiap 100ms
            # Jika jendela ditutup manual
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                print("Jendela ditutup manual. Keluar dari mode perbandingan.")
                cv2.destroyAllWindows()
                return
            if key != 255:
                print(f"Kode tombol ditekan: {key}")
                break

        # Cek tombol navigasi/keluar
        if key == ord('q') or key == 27: # q atau Esc
            print("\nKeluar dari mode perbandingan.")
            break
        # --- Kode Panah Kanan ---
        elif key == 83 or key == 67: # Kanan
             print("Panah Kanan terdeteksi")
             current_index = min(current_index + 1, len(image_pairs) - 1)
        # --- Kode Panah Kiri ---
        elif key == 81 or key == 68: # Kiri
             print("Panah Kiri terdeteksi")
             current_index = max(current_index - 1, 0)
        elif key != 255:
             print(f"Tombol tidak dikenal ditekan: Kode = {key}")
        # else: pass

    cv2.destroyAllWindows() # Tutup jendela setelah loop selesai

def run_processing_mode(input_dir, clip_limit, tile_grid_size):
    """Menjalankan mode pemrosesan CLAHE."""
    print("Memulai mode pemrosesan CLAHE...")
    # Periksa apakah direktori input ada
    if not os.path.isdir(input_dir):
        print(f"Error: Direktori input tidak ditemukan: {input_dir}")
        return

    # Buat nama dan path direktori output secara otomatis
    input_dir_norm = os.path.normpath(input_dir)
    input_base_name = os.path.basename(input_dir_norm)
    parent_dir = os.path.dirname(input_dir_norm)
    output_dir_name = f"{input_base_name}_clahe_output"
    output_dir = os.path.join(parent_dir if parent_dir else '.', output_dir_name)

    # Buat direktori output jika belum ada
    os.makedirs(output_dir, exist_ok=True)
    print(f"Direktori output (otomatis): {output_dir}")

    processed_count = 0
    error_count = 0
    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')

    # Iterasi melalui file di direktori input
    print(f"Memulai pemrosesan gambar di: {input_dir}")
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_extensions):
            input_path = os.path.join(input_dir, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_clahe{os.path.splitext(filename)[1]}"
            output_path = os.path.join(output_dir, output_filename)

            if process_image(input_path, output_path, clip_limit, tile_grid_size):
                processed_count += 1
            else:
                error_count += 1
        else:
            print(f"Skipping non-image file: {filename}")

    print(f"\nPemrosesan selesai.")
    print(f"Total gambar diproses: {processed_count}")
    print(f"Total error: {error_count}")


def main():
    parser = argparse.ArgumentParser(description="Terapkan CLAHE atau bandingkan hasil pada gambar dalam direktori.")
    parser.add_argument('--input_dir', type=str, required=True, help='Direktori berisi gambar input.')
    parser.add_argument('--output_dir', type=str, help='Direktori berisi gambar hasil (hanya digunakan dengan --compare).')
    parser.add_argument('--clip_limit', type=float, default=2.0, help='Batas kontras untuk CLAHE (mode proses, default: 2.0).')
    parser.add_argument('--tile_grid_size', type=int, nargs=2, default=[8, 8], metavar=('HEIGHT', 'WIDTH'), help='Ukuran grid tile untuk CLAHE (mode proses, default: 8 8).')
    parser.add_argument('--compare', action='store_true', help='Jalankan mode perbandingan (memerlukan --output_dir).')

    args = parser.parse_args()

    if args.compare:
        # Mode Perbandingan
        if not args.output_dir:
            parser.error("--output_dir diperlukan saat menggunakan --compare.")
        run_comparison_mode(args.input_dir, args.output_dir)
    else:
        # Mode Pemrosesan (Default)
        if args.output_dir:
             print("Warning: --output_dir diabaikan karena tidak dalam mode --compare. Direktori output akan dibuat otomatis.")
        run_processing_mode(args.input_dir, args.clip_limit, tuple(args.tile_grid_size))

if __name__ == "__main__":
    main()