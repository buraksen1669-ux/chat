import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "instagram_takip_data.json"

SABIT_ONERILER = {
    "Pazartesi": "Laptop bakım öncesi/sonrası karşılaştırma paylaş.",
    "Salı": "SSD yükseltme avantajları (hız testi videosu).",
    "Çarşamba": "Müşteri yorumu + kısa başarı hikayesi yayınla.",
    "Perşembe": "2. el bilgisayar alırken dikkat edilecek 5 madde.",
    "Cuma": "Hafta sonu kampanyası: format + bakım paketi.",
    "Cumartesi": "Canlı soru-cevap: bilgisayar yavaşlama sorunları.",
    "Pazar": "Haftalık özet + gelecek hafta teaser içeriği."
}

HASHTAG_SETI = [
    "#bilgisayartamiri", "#laptoptamiri", "#pcservis", "#istanbulbilgisayar",
    "#oyuncubilgisayari", "#teknikservis", "#bilgisayarsatis", "#ssdupgrade",
    "#formatatma", "#bilgisayarhizlandirma", "#turkiyeteknoloji", "#tamirhizmeti"
]

class Uygulama:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Instagram Büyütme ve Müşteri Yönetimi")
        self.root.geometry("1120x720")
        self.root.minsize(980, 620)

        self.veri = self.veri_yukle()

        self.stil_ayarla()
        self.ana_cerceve = ttk.Frame(self.root, padding=16)
        self.ana_cerceve.pack(fill="both", expand=True)

        self.baslik_olustur()
        self.notebook = ttk.Notebook(self.ana_cerceve)
        self.notebook.pack(fill="both", expand=True, pady=(8, 0))

        self.dashboard_tab = ttk.Frame(self.notebook, padding=12)
        self.icerik_tab = ttk.Frame(self.notebook, padding=12)
        self.musteri_tab = ttk.Frame(self.notebook, padding=12)
        self.analiz_tab = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(self.dashboard_tab, text="Kontrol Paneli")
        self.notebook.add(self.icerik_tab, text="İçerik Planı")
        self.notebook.add(self.musteri_tab, text="Müşteri Takibi")
        self.notebook.add(self.analiz_tab, text="Analiz")

        self.dashboard_olustur()
        self.icerik_tab_olustur()
        self.musteri_tab_olustur()
        self.analiz_tab_olustur()

        self.kartlari_guncelle()
        self.icerik_liste_guncelle()
        self.musteri_liste_guncelle()
        self.etkilesim_tahmin_hesapla()

    def stil_ayarla(self) -> None:
        stil = ttk.Style()
        stil.theme_use("clam")
        stil.configure("TFrame", background="#f4f6fb")
        stil.configure("TLabel", background="#f4f6fb", font=("Segoe UI", 11))
        stil.configure("Baslik.TLabel", font=("Segoe UI", 19, "bold"), foreground="#1a2340")
        stil.configure("AltBaslik.TLabel", font=("Segoe UI", 10), foreground="#5a6785")
        stil.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        stil.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        stil.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def baslik_olustur(self) -> None:
        cerceve = ttk.Frame(self.ana_cerceve)
        cerceve.pack(fill="x")

        ttk.Label(cerceve, text="Instagram Büyütme Asistanı", style="Baslik.TLabel").pack(anchor="w")
        ttk.Label(
            cerceve,
            text="Hedef kitle: Türkiye | Sektör: Bilgisayar tamiri ve bilgisayar satışı",
            style="AltBaslik.TLabel",
        ).pack(anchor="w", pady=(2, 0))

    def dashboard_olustur(self) -> None:
        ust = ttk.Frame(self.dashboard_tab)
        ust.pack(fill="x", pady=(0, 12))

        self.kart_takipci = self.kpi_karti(ust, "Toplam Takipçi", "0")
        self.kart_musteri = self.kpi_karti(ust, "Potansiyel Müşteri", "0")
        self.kart_icerik = self.kpi_karti(ust, "Bu Hafta İçerik", "0")
        self.kart_donusum = self.kpi_karti(ust, "DM Dönüşüm %", "0")

        for kart in [self.kart_takipci, self.kart_musteri, self.kart_icerik, self.kart_donusum]:
            kart.pack(side="left", fill="x", expand=True, padx=6)

        alt = ttk.LabelFrame(self.dashboard_tab, text="Bugünün İçerik Önerisi", padding=12)
        alt.pack(fill="x")

        gun = datetime.now().strftime("%A")
        gun_map = {
            "Monday": "Pazartesi", "Tuesday": "Salı", "Wednesday": "Çarşamba",
            "Thursday": "Perşembe", "Friday": "Cuma", "Saturday": "Cumartesi", "Sunday": "Pazar"
        }
        tr_gun = gun_map.get(gun, "Pazartesi")

        ttk.Label(alt, text=f"{tr_gun}: {SABIT_ONERILER[tr_gun]}", wraplength=900).pack(anchor="w")

    def kpi_karti(self, parent, baslik: str, deger: str) -> ttk.Frame:
        kart = ttk.Frame(parent, padding=12)
        ttk.Label(kart, text=baslik, style="AltBaslik.TLabel").pack(anchor="w")
        etiket = ttk.Label(kart, text=deger, font=("Segoe UI", 22, "bold"), foreground="#24355f")
        etiket.pack(anchor="w", pady=(4, 0))
        kart.deger_etiketi = etiket
        return kart

    def icerik_tab_olustur(self) -> None:
        form = ttk.LabelFrame(self.icerik_tab, text="Yeni İçerik Ekle", padding=12)
        form.pack(fill="x")

        ttk.Label(form, text="İçerik Başlığı").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.icerik_baslik = ttk.Entry(form, width=40)
        self.icerik_baslik.grid(row=0, column=1, sticky="ew", padx=4, pady=4)

        ttk.Label(form, text="Format").grid(row=0, column=2, sticky="w", padx=4, pady=4)
        self.icerik_format = ttk.Combobox(form, values=["Reels", "Carousel", "Hikaye", "Canlı Yayın"], state="readonly")
        self.icerik_format.set("Reels")
        self.icerik_format.grid(row=0, column=3, sticky="ew", padx=4, pady=4)

        ttk.Label(form, text="Yayın Tarihi").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.icerik_tarih = ttk.Entry(form)
        self.icerik_tarih.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.icerik_tarih.grid(row=1, column=1, sticky="ew", padx=4, pady=4)

        ttk.Label(form, text="Durum").grid(row=1, column=2, sticky="w", padx=4, pady=4)
        self.icerik_durum = ttk.Combobox(form, values=["Taslak", "Planlandı", "Yayınlandı"], state="readonly")
        self.icerik_durum.set("Taslak")
        self.icerik_durum.grid(row=1, column=3, sticky="ew", padx=4, pady=4)

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        ttk.Button(form, text="İçeriği Kaydet", command=self.icerik_ekle).grid(row=2, column=0, columnspan=4, pady=8)

        tablo = ttk.LabelFrame(self.icerik_tab, text="Planlanan İçerikler", padding=8)
        tablo.pack(fill="both", expand=True, pady=(10, 0))

        kolonlar = ("baslik", "format", "tarih", "durum")
        self.icerik_tree = ttk.Treeview(tablo, columns=kolonlar, show="headings")
        basliklar = ["Başlık", "Format", "Tarih", "Durum"]
        for key, text in zip(kolonlar, basliklar):
            self.icerik_tree.heading(key, text=text)
            self.icerik_tree.column(key, width=160)
        self.icerik_tree.pack(fill="both", expand=True)

    def musteri_tab_olustur(self) -> None:
        form = ttk.LabelFrame(self.musteri_tab, text="Yeni Potansiyel Müşteri", padding=12)
        form.pack(fill="x")

        ttk.Label(form, text="İsim").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.musteri_isim = ttk.Entry(form)
        self.musteri_isim.grid(row=0, column=1, sticky="ew", padx=4, pady=4)

        ttk.Label(form, text="İhtiyaç").grid(row=0, column=2, sticky="w", padx=4, pady=4)
        self.musteri_ihtiyac = ttk.Combobox(
            form,
            values=["Laptop Tamiri", "Masaüstü Tamiri", "Yeni Bilgisayar Satışı", "2. El Bilgisayar", "Parça Yükseltme"],
            state="readonly",
        )
        self.musteri_ihtiyac.set("Laptop Tamiri")
        self.musteri_ihtiyac.grid(row=0, column=3, sticky="ew", padx=4, pady=4)

        ttk.Label(form, text="Kaynak").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.musteri_kaynak = ttk.Combobox(form, values=["DM", "Yorum", "WhatsApp", "Referans"], state="readonly")
        self.musteri_kaynak.set("DM")
        self.musteri_kaynak.grid(row=1, column=1, sticky="ew", padx=4, pady=4)

        ttk.Label(form, text="Durum").grid(row=1, column=2, sticky="w", padx=4, pady=4)
        self.musteri_durum = ttk.Combobox(form, values=["Yeni", "Görüşüldü", "Teklif Verildi", "Satışa Döndü"], state="readonly")
        self.musteri_durum.set("Yeni")
        self.musteri_durum.grid(row=1, column=3, sticky="ew", padx=4, pady=4)

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        ttk.Button(form, text="Müşteri Ekle", command=self.musteri_ekle).grid(row=2, column=0, columnspan=4, pady=8)

        tablo = ttk.LabelFrame(self.musteri_tab, text="Müşteri Listesi", padding=8)
        tablo.pack(fill="both", expand=True, pady=(10, 0))

        kolonlar = ("isim", "ihtiyac", "kaynak", "durum", "tarih")
        self.musteri_tree = ttk.Treeview(tablo, columns=kolonlar, show="headings")
        basliklar = ["İsim", "İhtiyaç", "Kaynak", "Durum", "Kayıt Tarihi"]
        for key, text in zip(kolonlar, basliklar):
            self.musteri_tree.heading(key, text=text)
            self.musteri_tree.column(key, width=150)
        self.musteri_tree.pack(fill="both", expand=True)

    def analiz_tab_olustur(self) -> None:
        cerceve = ttk.Frame(self.analiz_tab)
        cerceve.pack(fill="both", expand=True)

        ttk.Label(cerceve, text="Hashtag Önerileri", style="Baslik.TLabel").pack(anchor="w")
        ttk.Label(
            cerceve,
            text="Bilgisayar tamiri/satışı içeriklerinde dönüşüm için yüksek niyetli etiketler:",
            style="AltBaslik.TLabel",
        ).pack(anchor="w", pady=(0, 6))

        self.hashtag_metin = tk.Text(cerceve, height=6, wrap="word", font=("Consolas", 11))
        self.hashtag_metin.pack(fill="x")
        self.hashtag_metin.insert("1.0", " ".join(HASHTAG_SETI))

        tahmin = ttk.LabelFrame(cerceve, text="Etkileşim Tahmini", padding=12)
        tahmin.pack(fill="x", pady=(12, 0))

        ttk.Label(tahmin, text="Haftalık Reels Sayısı").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.reels_sayisi = ttk.Entry(tahmin)
        self.reels_sayisi.insert(0, "4")
        self.reels_sayisi.grid(row=0, column=1, sticky="ew", padx=4, pady=4)

        ttk.Label(tahmin, text="Haftalık Hikaye Sayısı").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.hikaye_sayisi = ttk.Entry(tahmin)
        self.hikaye_sayisi.insert(0, "10")
        self.hikaye_sayisi.grid(row=1, column=1, sticky="ew", padx=4, pady=4)

        ttk.Button(tahmin, text="Tahmini Hesapla", command=self.etkilesim_tahmin_hesapla).grid(row=2, column=0, columnspan=2, pady=8)

        self.tahmin_sonuc = ttk.Label(tahmin, text="")
        self.tahmin_sonuc.grid(row=3, column=0, columnspan=2, sticky="w", padx=4)

        tahmin.columnconfigure(1, weight=1)

    def veri_yukle(self) -> dict:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"icerikler": [], "musteriler": [], "takipci": 0}

    def veri_kaydet(self) -> None:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.veri, f, ensure_ascii=False, indent=2)

    def icerik_ekle(self) -> None:
        baslik = self.icerik_baslik.get().strip()
        if not baslik:
            messagebox.showwarning("Uyarı", "İçerik başlığı boş olamaz.")
            return

        item = {
            "baslik": baslik,
            "format": self.icerik_format.get(),
            "tarih": self.icerik_tarih.get().strip(),
            "durum": self.icerik_durum.get(),
        }
        self.veri["icerikler"].append(item)
        self.veri_kaydet()
        self.icerik_baslik.delete(0, "end")
        self.icerik_liste_guncelle()
        self.kartlari_guncelle()

    def musteri_ekle(self) -> None:
        isim = self.musteri_isim.get().strip()
        if not isim:
            messagebox.showwarning("Uyarı", "Müşteri ismi boş olamaz.")
            return

        item = {
            "isim": isim,
            "ihtiyac": self.musteri_ihtiyac.get(),
            "kaynak": self.musteri_kaynak.get(),
            "durum": self.musteri_durum.get(),
            "tarih": datetime.now().strftime("%Y-%m-%d"),
        }
        self.veri["musteriler"].append(item)
        if self.musteri_durum.get() == "Satışa Döndü":
            self.veri["takipci"] += 8

        self.veri_kaydet()
        self.musteri_isim.delete(0, "end")
        self.musteri_liste_guncelle()
        self.kartlari_guncelle()

    def icerik_liste_guncelle(self) -> None:
        for i in self.icerik_tree.get_children():
            self.icerik_tree.delete(i)
        for row in self.veri["icerikler"]:
            self.icerik_tree.insert("", "end", values=(row["baslik"], row["format"], row["tarih"], row["durum"]))

    def musteri_liste_guncelle(self) -> None:
        for i in self.musteri_tree.get_children():
            self.musteri_tree.delete(i)
        for row in self.veri["musteriler"]:
            self.musteri_tree.insert(
                "", "end", values=(row["isim"], row["ihtiyac"], row["kaynak"], row["durum"], row["tarih"])
            )

    def kartlari_guncelle(self) -> None:
        takipci = self.veri["takipci"]
        musteri = len(self.veri["musteriler"])
        icerik = len([i for i in self.veri["icerikler"] if i["durum"] in {"Planlandı", "Yayınlandı"}])
        donusum = 0
        if musteri:
            donusum_sayisi = len([m for m in self.veri["musteriler"] if m["durum"] == "Satışa Döndü"])
            donusum = int((donusum_sayisi / musteri) * 100)

        self.kart_takipci.deger_etiketi.config(text=str(takipci))
        self.kart_musteri.deger_etiketi.config(text=str(musteri))
        self.kart_icerik.deger_etiketi.config(text=str(icerik))
        self.kart_donusum.deger_etiketi.config(text=f"%{donusum}")

    def etkilesim_tahmin_hesapla(self) -> None:
        try:
            reels = int(self.reels_sayisi.get())
            hikaye = int(self.hikaye_sayisi.get())
        except ValueError:
            messagebox.showwarning("Uyarı", "Lütfen reels ve hikaye sayıları için sayı girin.")
            return

        tahmini_erisim = reels * 1200 + hikaye * 250
        tahmini_dm = max(5, int(tahmini_erisim * 0.012))
        tahmini_satis = max(1, int(tahmini_dm * 0.18))

        self.tahmin_sonuc.config(
            text=(
                f"Tahmini haftalık erişim: {tahmini_erisim} | "
                f"Tahmini DM: {tahmini_dm} | "
                f"Tahmini sıcak müşteri: {tahmini_satis}"
            )
        )


def main() -> None:
    root = tk.Tk()
    Uygulama(root)
    root.mainloop()


if __name__ == "__main__":
    main()
