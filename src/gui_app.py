import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from deret_harmonik import hitung_deret_harmonik, validasi_input
from history_manager import HistoryManager

class DeretHarmonikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deret Harmonik")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Inisialisasi history manager
        self.history_manager = HistoryManager()
        
        # Setup style
        self.setup_styles()
        
        # Buat GUI
        self.create_widgets()
        
        # Tampilkan riwayat terbaru
        self.refresh_history()
    
    def setup_styles(self):
        """Mengatur style untuk widget"""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', background='#f0f0f0', font=('Arial', 16, 'bold'))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Success.TButton', background='#4CAF50', foreground='white')
        style.configure('Secondary.TButton', background='#607D8B', foreground='white')
    
    def create_widgets(self):
        """Membuat semua widget GUI"""
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Judul
        title_label = ttk.Label(main_frame, text="DERET HARMONIK", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Frame input
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Masukkan bilangan bulat positif N:").pack(anchor=tk.W)
        
        # Frame untuk input dan tombol
        input_button_frame = ttk.Frame(input_frame)
        input_button_frame.pack(fill=tk.X, pady=5)
        
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(input_button_frame, textvariable=self.entry_var, font=('Arial', 12), width=20)
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
        self.entry.bind('<Return>', lambda e: self.hitung_deret())
        
        self.hitung_button = ttk.Button(input_button_frame, text="Hitung Deret", command=self.hitung_deret)
        self.hitung_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(input_button_frame, text="Bersihkan", command=self.clear_input)
        self.clear_button.pack(side=tk.LEFT)
        
        # Frame hasil
        hasil_frame = ttk.LabelFrame(main_frame, text="Hasil Perhitungan", padding="10")
        hasil_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.hasil_text = scrolledtext.ScrolledText(hasil_frame, height=6, font=('Consolas', 10), wrap=tk.WORD)
        self.hasil_text.pack(fill=tk.BOTH, expand=True)
        self.hasil_text.config(state=tk.DISABLED)
        
        # Frame riwayat
        history_frame = ttk.LabelFrame(main_frame, text="Riwayat Perhitungan (10 Terbaru)", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Toolbar riwayat
        history_toolbar = ttk.Frame(history_frame)
        history_toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(history_toolbar, text="Refresh", command=self.refresh_history).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(history_toolbar, text="Hapus Riwayat", command=self.clear_history).pack(side=tk.LEFT)
        
        # Tabel riwayat
        columns = ('No', 'Waktu', 'N', 'Hasil')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=8)
        
        # Define headings
        self.history_tree.heading('No', text='No')
        self.history_tree.heading('Waktu', text='Waktu')
        self.history_tree.heading('N', text='N')
        self.history_tree.heading('Hasil', text='Hasil')
        
        # Define columns
        self.history_tree.column('No', width=50)
        self.history_tree.column('Waktu', width=150)
        self.history_tree.column('N', width=80)
        self.history_tree.column('Hasil', width=200)
        
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double click event
        self.history_tree.bind('<Double-1>', self.on_history_double_click)
        
        # Status bar
        self.status_var = tk.StringVar(value="Siap menerima input...")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def hitung_deret(self):
        """Menghitung deret harmonik"""
        input_str = self.entry_var.get().strip()
        
        # Validasi input
        valid, n, message = validasi_input(input_str)
        if not valid:
            messagebox.showerror("Error Input", message)
            return
        
        # Nonaktifkan tombol selama perhitungan
        self.hitung_button.config(state=tk.DISABLED)
        self.status_var.set("Menghitung deret harmonik...")
        
        # Jalankan perhitungan di thread terpisah untuk mencegah GUI freeze
        def calculate():
            try:
                hasil, penjabaran = hitung_deret_harmonik(n)
                
                # Update GUI di main thread
                self.root.after(0, self.update_hasil, n, hasil, penjabaran)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"Terjadi kesalahan: {str(e)}")
            finally:
                self.root.after(0, self.enable_hitung_button)
        
        thread = threading.Thread(target=calculate)
        thread.daemon = True
        thread.start()
    
    def update_hasil(self, n, hasil, penjabaran):
        """Update tampilan hasil perhitungan"""
        # Tampilkan hasil
        self.hasil_text.config(state=tk.NORMAL)
        self.hasil_text.delete(1.0, tk.END)
        
        hasil_str = f"Deret Harmonik untuk N = {n}\n\n"
        hasil_str += f"Penjabaran:\n{penjabaran}\n\n"
        hasil_str += f"Hasil: {hasil:.12f}\n"
        
        self.hasil_text.insert(tk.END, hasil_str)
        self.hasil_text.config(state=tk.DISABLED)
        
        # Tambahkan ke riwayat
        self.history_manager.add_calculation(n, float(hasil), penjabaran)
        
        # Refresh tampilan riwayat
        self.refresh_history()
        
        self.status_var.set(f"Perhitungan selesai untuk N = {n}")
    
    def show_error(self, message):
        """Menampilkan pesan error"""
        messagebox.showerror("Error", message)
        self.status_var.set("Terjadi kesalahan dalam perhitungan")
    
    def enable_hitung_button(self):
        """Mengaktifkan kembali tombol hitung"""
        self.hitung_button.config(state=tk.NORMAL)
    
    def clear_input(self):
        """Membersihkan input dan hasil"""
        self.entry_var.set("")
        self.hasil_text.config(state=tk.NORMAL)
        self.hasil_text.delete(1.0, tk.END)
        self.hasil_text.config(state=tk.DISABLED)
        self.status_var.set("Input telah dibersihkan")
    
    def refresh_history(self):
        """Memperbarui tampilan riwayat"""
        # Hapus data lama
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Tambahkan data baru
        history = self.history_manager.get_history(10)
        for i, entry in enumerate(history, 1):
            self.history_tree.insert('', tk.END, values=(
                i,
                entry['timestamp'],
                entry['n'],
                f"{entry['hasil']:.6f}"
            ))
    
    def clear_history(self):
        """Menghapus semua riwayat"""
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua riwayat?"):
            self.history_manager.clear_history()
            self.refresh_history()
            self.status_var.set("Riwayat telah dihapus")
    
    def on_history_double_click(self, event):
        """Event handler untuk double click pada riwayat"""
        selection = self.history_tree.selection()
        if selection:
            item = selection[0]
            values = self.history_tree.item(item, 'values')
            if values:
                # Isi input dengan nilai N dari riwayat
                n_value = values[2]  # Kolom N
                self.entry_var.set(n_value)
                self.status_var.set(f"Input diisi dengan N = {n_value} dari riwayat")


def run_gui():
    """Menjalankan aplikasi GUI"""
    root = tk.Tk()
    app = DeretHarmonikApp(root)
    root.mainloop()