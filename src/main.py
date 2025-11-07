import sys
import argparse
from deret_harmonik import hitung_deret_harmonik, validasi_input
from history_manager import HistoryManager

def main_cli():
    """Fungsi utama mode CLI"""
    print("=" * 50)
    print("DERET HARMONIK")
    print("=" * 50)
    
    history_manager = HistoryManager()
    
    while True:
        print("\nPilihan Menu:")
        print("1. Hitung Deret Harmonik")
        print("2. Lihat Riwayat")
        print("3. Hapus Riwayat")
        print("4. Keluar")
        
        pilihan = input("\nMasukkan pilihan (1-4): ").strip()
        
        if pilihan == "1":
            hitung_deret_menu(history_manager)
        elif pilihan == "2":
            lihat_riwayat_menu(history_manager)
        elif pilihan == "3":
            hapus_riwayat_menu(history_manager)
        elif pilihan == "4":
            print("Terima kasih telah menggunakan program!")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih 1-4.")


def hitung_deret_menu(history_manager):
    """Menu untuk menghitung deret harmonik"""
    print("\n" + "-" * 40)
    print("HITUNG DERET HARMONIK")
    print("-" * 40)
    
    input_n = input("Masukkan bilangan bulat positif N: ").strip()
    
    # Validasi input
    valid, n, message = validasi_input(input_n)
    if not valid:
        print(f"Error: {message}")
        return
    
    # Hitung deret harmonik
    try:
        hasil, penjabaran = hitung_deret_harmonik(n)
        
        # Tampilkan hasil
        print(f"\nHasil Perhitungan untuk N = {n}:")
        print(f"Deret: {penjabaran}")
        print(f"Hasil: {hasil:.12f}")
        
        # Simpan ke riwayat
        history_manager.add_calculation(n, float(hasil), penjabaran)
        print("✓ Perhitungan telah disimpan ke riwayat")
        
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")


def lihat_riwayat_menu(history_manager):
    """Menu untuk melihat riwayat perhitungan"""
    print("\n" + "-" * 40)
    print("RIWAYAT PERHITUNGAN")
    print("-" * 40)
    
    history = history_manager.get_history(10)
    
    if not history:
        print("Belum ada riwayat perhitungan.")
        return
    
    print(f"{'No':<3} {'Waktu':<19} {'N':<6} {'Hasil':<15}")
    print("-" * 50)
    
    for i, entry in enumerate(history, 1):
        print(f"{i:<3} {entry['timestamp']:<19} {entry['n']:<6} {entry['hasil']:<15.6f}")


def hapus_riwayat_menu(history_manager):
    """Menu untuk menghapus riwayat"""
    print("\n" + "-" * 40)
    print("HAPUS RIWAYAT")
    print("-" * 40)
    
    konfirmasi = input("Apakah Anda yakin ingin menghapus semua riwayat? (y/N): ").strip().lower()
    
    if konfirmasi == 'y':
        history_manager.clear_history()
        print("✓ Riwayat telah dihapus")
    else:
        print("Penghapusan riwayat dibatalkan")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Program Deret Harmonik')
    parser.add_argument('--gui', action='store_true', help='Jalankan dalam mode GUI')
    parser.add_argument('--cli', action='store_true', help='Jalankan dalam mode CLI')
    
    args = parser.parse_args()
    
    if args.gui or (not args.cli and not args.gui):
        # Default ke GUI jika tidak ada argumen atau --gui diberikan
        try:
            from gui_app import run_gui
            run_gui()
        except ImportError as e:
            print("Error: Tidak dapat menjalankan mode GUI")
            print("Pastikan semua modul tersedia")
            sys.exit(1)
    else:
        # Jalankan mode CLI
        main_cli()