import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, filename="history_deret_harmonik.json"):
        self.filename = filename
        self.history = []
        self.load_history()
    
    def load_history(self):
        """Memuat riwayat dari file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, Exception):
                self.history = []
    
    def save_history(self):
        """Menyimpan riwayat ke file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error menyimpan history: {e}")
    
    def add_calculation(self, n, hasil, penjabaran):
        """Menambahkan perhitungan ke riwayat"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "n": n,
            "hasil": hasil,
            "penjabaran": penjabaran
        }
        self.history.insert(0, entry)  # Tambahkan di awal
        
        # Batasi riwayat menjadi 50 entri terakhir
        if len(self.history) > 50:
            self.history = self.history[:50]
        
        self.save_history()
    
    def get_history(self, limit=10):
        """Mendapatkan riwayat perhitungan"""
        return self.history[:limit]
    
    def clear_history(self):
        """Menghapus semua riwayat"""
        self.history = []
        self.save_history()