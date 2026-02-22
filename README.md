# Instagram Büyütme ve Müşteri Yönetimi (Windows)

Bu proje, **Türk hedef kitleye** (özellikle bilgisayar tamiri ve bilgisayar satışı alanında) yönelik Instagram hesabını daha planlı yönetmek için geliştirilmiş masaüstü bir Python uygulamasıdır.

## Özellikler
- Türkçe arayüz (Tkinter tabanlı)
- İçerik planlama (Reels / Hikaye / Carousel)
- Potansiyel müşteri takip ekranı
- Basit dönüşüm ve KPI paneli
- Sektöre uygun hashtag önerileri
- İçerik ve müşteri verilerini yerel JSON dosyasında saklama

## Çalıştırma
```bash
python app.py
```

## Windows EXE'ye Dönüştürme (PyInstaller)
1. Sanal ortam oluşturun (önerilir)
2. PyInstaller kurun:
   ```bash
   pip install pyinstaller
   ```
3. EXE üretin:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --name InstaBuyutme app.py
   ```
4. Çıktı dosyası: `dist/InstaBuyutme.exe`

## Not
Uygulama ilk çalıştırmada aynı klasöre `instagram_takip_data.json` dosyasını otomatik oluşturur.
