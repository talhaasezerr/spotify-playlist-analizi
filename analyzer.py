"""
Spotify Playlist Analyzer
"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import Counter
from typing import List, Dict, Optional

class SpotifyAnalyzer:
    def __init__(self, client_id: str, client_secret: str):
        """
        Spotify API bağlantısını başlat
        
        Args:
            client_id: Spotify Client ID
            client_secret: Spotify Client Secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        
        # Spotify Client Credentials akışı ile bağlan
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
    
    def get_user_playlists(self, username: str = "spotify") -> List[Dict]:
        """
        Kullanıcının playlist'lerini al
        
        Args:
            username: Spotify kullanıcı adı (varsayılan: "spotify" - featured playlists)
        
        Returns:
            Playlist bilgileri listesi
        """
        try:
            playlists = []
            
            # Featured playlists'i al (herkes için erişilebilir)
            results = self.sp.featured_playlists(limit=50)
            
            for playlist in results['playlists']['items']:
                playlists.append({
                    'id': playlist['id'],
                    'name': playlist['name'],
                    'tracks': playlist['tracks']['total'],
                    'owner': playlist['owner']['display_name']
                })
            
            return playlists
        except Exception as e:
            print(f"Playlist alma hatası: {e}")
            return []
    
    def analyze_playlist(self, playlist_id: str) -> Optional[Dict]:
        """
        Playlist'i analiz et
        
        Args:
            playlist_id: Playlist ID
        
        Returns:
            Analiz sonuçları
        """
        try:
            # Playlist track'lerini al
            results = self.sp.playlist_tracks(playlist_id)
            tracks = results['items']
            
            # Tüm track'leri al (pagination)
            while results['next']:
                results = self.sp.next(results)
                tracks.extend(results['items'])
            
            if not tracks:
                return None
            
            # Track ID'lerini ve sanatçı bilgilerini topla
            track_ids = []
            artists = []
            
            for item in tracks:
                if item['track']:
                    track_ids.append(item['track']['id'])
                    for artist in item['track']['artists']:
                        artists.append(artist['name'])
            
            # Audio features al (batch olarak)
            audio_features = []
            batch_size = 100
            
            for i in range(0, len(track_ids), batch_size):
                batch = track_ids[i:i + batch_size]
                features_batch = self.sp.audio_features(batch)
                audio_features.extend([f for f in features_batch if f])
            
            if not audio_features:
                return None
            
            # Özellikleri hesapla
            energy = sum(f['energy'] for f in audio_features) / len(audio_features)
            danceability = sum(f['danceability'] for f in audio_features) / len(audio_features)
            valence = sum(f['valence'] for f in audio_features) / len(audio_features)
            tempo = sum(f['tempo'] for f in audio_features) / len(audio_features)
            acousticness = sum(f['acousticness'] for f in audio_features) / len(audio_features)
            speechiness = sum(f['speechiness'] for f in audio_features) / len(audio_features)
            
            # Mood belirle
            mood = self._determine_mood(energy, valence, tempo)
            
            # En çok dinlenen sanatçılar
            artist_counts = Counter(artists)
            top_artists = artist_counts.most_common(10)
            
            return {
                'total_tracks': len(tracks),
                'unique_artists': len(set(artists)),
                'mood': mood,
                'energy_avg': energy,
                'danceability_avg': danceability,
                'valence_avg': valence,
                'tempo_avg': tempo,
                'acousticness_avg': acousticness,
                'speechiness_avg': speechiness,
                'top_artists': top_artists
            }
        
        except Exception as e:
            print(f"Analiz hatası: {e}")
            return None
    
    def _determine_mood(self, energy: float, valence: float, tempo: float) -> str:
        """
        Playlist mood'unu belirle
        
        Args:
            energy: Enerji seviyesi (0-1)
            valence: Pozitiflik seviyesi (0-1)
            tempo: Tempo (BPM)
        
        Returns:
            Mood açıklaması
        """
        # Enerjili ve mutlu
        if energy > 0.7 and valence > 0.7:
            return "🔥 Enerjik ve Neşeli"
        
        # Enerjili ama hüzünlü
        elif energy > 0.7 and valence < 0.3:
            return "⚡ Enerjik ama Melankolik"
        
        # Sakin ve mutlu
        elif energy < 0.4 and valence > 0.7:
            return "😌 Rahatlatıcı ve Pozitif"
        
        # Sakin ve hüzünlü
        elif energy < 0.4 and valence < 0.3:
            return "😔 Sakin ve Melankolik"
        
        # Orta tempo ve mutlu
        elif valence > 0.6:
            return "😊 Pozitif ve Dengeli"
        
        # Orta tempo ve hüzünlü
        elif valence < 0.4:
            return "🎭 Duygusal ve İçten"
        
        else:
            return "🎵 Dengeli Mix"
    
    def search_playlists(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Playlist ara
        
        Args:
            query: Arama terimi
            limit: Maksimum sonuç sayısı
        
        Returns:
            Bulunan playlist'ler
        """
        try:
            results = self.sp.search(q=query, type='playlist', limit=limit)
            
            playlists = []
            for playlist in results['playlists']['items']:
                playlists.append({
                    'id': playlist['id'],
                    'name': playlist['name'],
                    'tracks': playlist['tracks']['total'],
                    'owner': playlist['owner']['display_name']
                })
            
            return playlists
        
        except Exception as e:
            print(f"Arama hatası: {e}")
            return []
