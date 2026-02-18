"""
Spotify Playlist Analiz Aracı - GUI
"""
import customtkinter as ctk
from tkinter import messagebox
import threading
from analyzer import SpotifyAnalyzer
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# .env dosyasını yükle
load_dotenv()

class SpotifyAnalyzerApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🎵 Spotify Playlist Analiz")
        self.window.geometry("1000x800")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        self.analyzer = None
        self.playlists = []
        self.setup_ui()
    
    def setup_ui(self):
        """Arayüzü oluştur"""
        # Başlık
        title = ctk.CTkLabel(
            self.window,
            text="🎵 Spotify Playlist Analiz",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        # API Credentials Frame
        cred_frame = ctk.CTkFrame(self.window)
        cred_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(cred_frame, text="Spotify API Credentials", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        # Client ID
        id_frame = ctk.CTkFrame(cred_frame)
        id_frame.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(id_frame, text="Client ID:", width=100).pack(side="left", padx=5)
        self.client_id_entry = ctk.CTkEntry(id_frame, width=400)
        self.client_id_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # .env'den yükle
        if os.getenv("SPOTIFY_CLIENT_ID"):
            self.client_id_entry.insert(0, os.getenv("SPOTIFY_CLIENT_ID"))
        
        # Client Secret
        secret_frame = ctk.CTkFrame(cred_frame)
        secret_frame.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(secret_frame, text="Client Secret:", width=100).pack(side="left", padx=5)
        self.client_secret_entry = ctk.CTkEntry(secret_frame, width=400, show="*")
        self.client_secret_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        if os.getenv("SPOTIFY_CLIENT_SECRET"):
            self.client_secret_entry.insert(0, os.getenv("SPOTIFY_CLIENT_SECRET"))
        
        # Bağlan butonu
        self.connect_btn = ctk.CTkButton(
            cred_frame,
            text="🔗 Spotify'a Bağlan",
            command=self.connect_spotify,
            height=35
        )
        self.connect_btn.pack(pady=10)
        
        # Playlist seçimi
        playlist_frame = ctk.CTkFrame(self.window)
        playlist_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(playlist_frame, text="Playlist Seç:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)
        
        self.playlist_var = ctk.StringVar(value="Önce bağlanın...")
        self.playlist_menu = ctk.CTkOptionMenu(
            playlist_frame,
            values=["Önce bağlanın..."],
            variable=self.playlist_var,
            width=300,
            state="disabled"
        )
        self.playlist_menu.pack(side="left", padx=5)
        
        self.analyze_btn = ctk.CTkButton(
            playlist_frame,
            text="📊 Analiz Et",
            command=self.analyze_playlist,
            state="disabled"
        )
        self.analyze_btn.pack(side="left", padx=5)
        
        # Sonuçlar
        results_frame = ctk.CTkFrame(self.window)
        results_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(results_frame, text="📈 Analiz Sonuçları", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.results_text = ctk.CTkTextbox(results_frame, height=400)
        self.results_text.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Durum
        self.status_label = ctk.CTkLabel(self.window, text="Spotify'a bağlanın", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=10)
        
        # Info label
        info = ctk.CTkLabel(
            self.window,
            text="ℹ️ Spotify Developer Dashboard'dan Client ID ve Secret alın: developer.spotify.com",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info.pack(pady=5)
    
    def connect_spotify(self):
        """Spotify'a bağlan"""
        client_id = self.client_id_entry.get().strip()
        client_secret = self.client_secret_entry.get().strip()
        
        if not client_id or not client_secret:
            messagebox.showerror("Hata", "Client ID ve Secret girin!")
            return
        
        self.status_label.configure(text="⏳ Spotify'a bağlanılıyor...")
        self.connect_btn.configure(state="disabled")
        
        def connect():
            try:
                self.analyzer = SpotifyAnalyzer(client_id, client_secret)
                playlists = self.analyzer.get_user_playlists()
                
                if playlists:
                    self.playlists = playlists
                    self.window.after(0, self.connection_success)
                else:
                    self.window.after(0, lambda: self.connection_failed("Playlist bulunamadı"))
            except Exception as e:
                self.window.after(0, lambda: self.connection_failed(str(e)))
        
        threading.Thread(target=connect, daemon=True).start()
    
    def connection_success(self):
        """Bağlantı başarılı"""
        playlist_names = [f"{p['name']} ({p['tracks']} şarkı)" for p in self.playlists]
        
        self.playlist_menu.configure(values=playlist_names, state="normal")
        self.playlist_var.set(playlist_names[0])
        self.analyze_btn.configure(state="normal")
        
        self.status_label.configure(text=f"✅ Bağlandı! {len(self.playlists)} playlist bulundu")
        self.connect_btn.configure(state="normal", text="✅ Bağlı")
    
    def connection_failed(self, error):
        """Bağlantı başarısız"""
        self.status_label.configure(text=f"❌ Bağlantı hatası: {error}")
        self.connect_btn.configure(state="normal")
        messagebox.showerror("Bağlantı Hatası", f"Spotify'a bağlanılamadı:\n{error}")
    
    def analyze_playlist(self):
        """Playlist analiz et"""
        selected = self.playlist_var.get()
        
        if not selected or selected == "Önce bağlanın...":
            return
        
        # Seçilen playlist'i bul
        playlist_name = selected.split(" (")[0]
        playlist = next((p for p in self.playlists if p['name'] == playlist_name), None)
        
        if not playlist:
            return
        
        self.status_label.configure(text="⏳ Analiz ediliyor...")
        self.analyze_btn.configure(state="disabled")
        
        def analyze():
            try:
                analysis = self.analyzer.analyze_playlist(playlist['id'])
                if analysis:
                    self.window.after(0, lambda: self.show_results(analysis))
                else:
                    self.window.after(0, lambda: self.analysis_failed("Analiz yapılamadı"))
            except Exception as e:
                self.window.after(0, lambda: self.analysis_failed(str(e)))
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def show_results(self, analysis: dict):
        """Analiz sonuçlarını göster"""
        self.results_text.delete("1.0", "end")
        
        result = f"""
🎵 PLAYLIST ANALİZİ
{'='*50}

📊 GENEL BİLGİLER
• Toplam Şarkı: {analysis['total_tracks']}
• Farklı Sanatçı: {analysis['unique_artists']}
• Genel Mood: {analysis['mood']}

🎼 MÜZİK ÖZELLİKLERİ
• Enerji: {analysis.get('energy_avg', 0):.2%} (0-100%)
• Dans Edilebilirlik: {analysis.get('danceability_avg', 0):.2%}
• Mutluluk/Pozitiflik: {analysis.get('valence_avg', 0):.2%}
• Tempo: {analysis.get('tempo_avg', 0):.1f} BPM
• Akustiklik: {analysis.get('acousticness_avg', 0):.2%}
• Vokal Oranı: {analysis.get('speechiness_avg', 0):.2%}

🎤 EN ÇOK DİNLENEN SANATÇILAR (Top 10)
"""
        for i, (artist, count) in enumerate(analysis['top_artists'], 1):
            result += f"{i}. {artist} - {count} şarkı\n"
        
        result += "\n" + "="*50
        
        self.results_text.insert("1.0", result)
        
        self.status_label.configure(text="✅ Analiz tamamlandı!")
        self.analyze_btn.configure(state="normal")
    
    def analysis_failed(self, error):
        """Analiz başarısız"""
        self.status_label.configure(text=f"❌ Analiz hatası: {error}")
        self.analyze_btn.configure(state="normal")
        messagebox.showerror("Analiz Hatası", f"Playlist analiz edilemedi:\n{error}")
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.window.mainloop()

if __name__ == "__main__":
    app = SpotifyAnalyzerApp()
    app.run()