# InstaPilot (Windows için masaüstü uygulaması)

Bu proje, Instagram hesabını büyütmek isteyenler için Tkinter tabanlı bir masaüstü arayüzü sunar.

## Özellikler

- **Konu Tespiti**: Sayfanın konusunu, hedef kitlesini ve teklifini netleştirir.
- **İçerik Kontrolü**: İçerik fikirlerini format/hedef ile birlikte kaydeder.
- **Keşfet Radar**: Güncel keşfet formatlarını takip etmek için not alanı.
- **Büyüme Planı**: Haftalık büyüme önerileri.
- **Durum Kaydı**: Verileri `instagram_workspace.json` dosyasına kaydeder.

## Geliştirme için çalıştırma

```bash
python app.py
```

> Not: Python 3.10+ önerilir. Ek paket gerektirmez.

## EXE olarak alma (Windows)

### Hızlı yöntem

1. Proje klasöründe `build_exe.bat` dosyasını çift tıkla.
2. Script otomatik olarak:
   - `.venv` oluşturur,
   - `pyinstaller` kurar,
   - `InstaPilot.exe` üretir.
3. Çıktı dosyası: `dist\InstaPilot.exe`

### Manuel yöntem

```powershell
py -3 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name InstaPilot app.py
```

Çıktı yine `dist\InstaPilot.exe` altında oluşur.
