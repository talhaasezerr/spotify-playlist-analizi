# spotify-playlist-analizi
# 🎵 Spotify Playlist Analiz Aracı

Spotify playlist'lerinizi analiz eden modern GUI uygulaması. Playlist'inizdeki şarkıların enerji, dans edilebilirlik, tempo gibi özelliklerini görselleştirir.

## ✨ Özellikler

- 🎯 Spotify API ile bağlantı
- 📊 Detaylı playlist analizi
- 🎼 Müzik özellikleri (enerji, dans edilebilirlik, tempo, vb.)
- 🎤 En çok dinlenen sanatçılar
- 😊 Otomatik mood belirleme
- 🖥️ Modern ve kullanıcı dostu arayüz

## 📋 Gereksinimler

- Python 3.7+
- Spotify Developer hesabı

## 🚀 Kurulum

1. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

2. Spotify API Credentials alın:
   - [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)'a gidin
   - Yeni bir uygulama oluşturun
   - Client ID ve Client Secret'ı kopyalayın

3. `.env` dosyası oluşturun (opsiyonel):

```bash
# .env.example dosyasını kopyalayın
cp .env.example .env

# .env dosyasına credentials'larınızı girin
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

## 💻 Kullanım

Uygulamayı başlatın:

```bash
python spotify
```

### Adımlar:

1. **API Credentials Girin**: Client ID ve Secret'ı ilgili alanlara girin
2. **Bağlan**: "Spotify'a Bağlan" butonuna tıklayın
3. **Playlist Seç**: Açılan listeden analiz etmek istediğiniz playlist'i seçin
4. **Analiz Et**: "Analiz Et" butonuna tıklayın
5. **Sonuçları İnceleyin**: Detaylı analiz sonuçlarını görüntüleyin

## 📊 Analiz Özellikleri

Uygulama aşağıdaki özellikleri analiz eder:

- **Enerji**: Müziğin yoğunluğu ve aktivite seviyesi (0-100%)
- **Dans Edilebilirlik**: Ritim, tempo ve ritim istikrarına göre dans edilebilirlik (0-100%)
- **Mutluluk/Pozitiflik**: Müziğin pozitif veya negatif duygusal tonu (0-100%)
- **Tempo**: Ortalama tempo (BPM)
- **Akustiklik**: Akustik enstrüman kullanım oranı (0-100%)
- **Vokal Oranı**: Konuşma/şarkı sözü oranı (0-100%)

## 🎭 Mood Kategorileri

Uygulama şu mood'ları otomatik belirler:

- 🔥 **Enerjik ve Neşeli**: Yüksek enerji, yüksek pozitiflik
- ⚡ **Enerjik ama Melankolik**: Yüksek enerji, düşük pozitiflik
- 😌 **Rahatlatıcı ve Pozitif**: Düşük enerji, yüksek pozitiflik
- 😔 **Sakin ve Melankolik**: Düşük enerji, düşük pozitiflik
- 😊 **Pozitif ve Dengeli**: Orta seviye enerji, yüksek pozitiflik
- 🎭 **Duygusal ve İçten**: Orta seviye enerji, düşük pozitiflik
- 🎵 **Dengeli Mix**: Dengeli özelliklere sahip

## 📁 Proje Yapısı

```
playlist/
│
├── spotify              # Ana GUI uygulaması
├── analyzer.py          # Spotify API ve analiz mantığı
├── requirements.txt     # Gerekli kütüphaneler
├── .env.example         # .env dosyası şablonu
└── README.md           # Bu dosya
```

## 🔧 Teknik Detaylar

### Kullanılan Kütüphaneler

- **customtkinter**: Modern GUI arayüzü
- **spotipy**: Spotify API wrapper
- **python-dotenv**: Ortam değişkenleri yönetimi
- **matplotlib**: Veri görselleştirme (gelecek özellik)

### API Kullanımı

Uygulama Spotify'ın Client Credentials Flow'unu kullanır. Bu akış:
- Kullanıcı girişi gerektirmez
- Public playlists'e erişim sağlar
- Rate limit: 60 saniyede 180 istek

## ⚠️ Notlar

- Uygulama sadece public/featured playlists'lere erişebilir
- Private playlist analizi için User OAuth flow gerekir
- İlk kullanımda API ile bağlantı birkaç saniye sürebilir
- Büyük playlist'ler (500+ şarkı) analiz edilirken bekleyin

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Commit atın (`git commit -am 'Yeni özellik eklendi'`)
4. Push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## 📝 Lisans

MIT

## 💡 Gelecek Özellikler

- [ ] Grafik ve görselleştirmeler
- [ ] Playlist karşılaştırma
- [ ] Şarkı önerileri
- [ ] Playlist export/import
- [ ] User authentication ile kişisel playlist analizi
- [ ] Detaylı istatistikler ve raporlar

## 🐛 Bilinen Sorunlar

Herhangi bir sorun bulursanız lütfen GitHub Issues'da bildirin.

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

---

**🎵 Mutlu analizler!**
