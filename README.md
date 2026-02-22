# Instagram Analiz Uygulaması (PyQt5)

Bu proje, Windows üzerinde çalışacak şekilde hazırlanmış, Instagram Graph API tabanlı bir analiz uygulamasıdır.

## Özellikler

- Instagram hesabına **şifre saklamadan**, **access token** ile bağlanma
- Son 50 gönderiyi çekme
- Gönderi başına:
  - Beğeni sayısı
  - Yorum sayısı
  - Paylaşım tarihi
  - İçerik türü (Reels, Fotoğraf, Video)
- Etkileşim oranı hesaplama:
  - `engagement_rate = (beğeni + yorum) / takipçi sayısı`
- Analizler:
  - En yüksek etkileşim alan gönderiler
  - Saat bazlı etkileşim
  - İçerik türüne göre ortalama etkileşim
  - Takipçi artış grafiği (insights verisi varsa)
- Arayüz:
  - PyQt5 sekmeleri: Genel İstatistik, Gönderi Analizi, Grafikler
  - Matplotlib grafikler
  - "Verileri Güncelle" butonu
- Güvenlik:
  - Token dosyada şifreli (Fernet) saklanır
  - Hatalar try-except ile yakalanır

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Çalıştırma

```bash
python main.py
```

## PyInstaller ile .exe üretme (Windows)

```bash
pyinstaller --onefile --windowed --name insta_analyzer main.py
```

Oluşan `.exe` dosyası `dist/insta_analyzer.exe` altında olur.

## Notlar

- Instagram Graph API kullanımı için geçerli access token ve Instagram User ID gereklidir.
- Takipçi artış verisi için ilgili hesapta insights erişimi ve uygun izinler bulunmalıdır.
