import json
import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("instagram_workspace.json")


@dataclass
class NicheProfile:
    topic: str
    audience: str
    offer: str
    style: str

    def score(self) -> int:
        score = 0
        if self.topic.strip():
            score += 30
        if self.audience.strip():
            score += 25
        if self.offer.strip():
            score += 25
        if self.style.strip():
            score += 20
        return score


class InstagramGrowthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("InstaPilot - Instagram Yönetim Asistanı")
        self.geometry("1100x720")
        self.minsize(980, 640)

        self.content_items = []
        self.last_profile = None

        self._build_style()
        self._build_layout()
        self._load_state()

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background="#f4f6fb", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(16, 10), font=("Segoe UI", 10, "bold"))
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Header.TLabel", font=("Segoe UI", 15, "bold"), background="#ffffff")
        style.configure("Muted.TLabel", foreground="#666", background="#ffffff")

    def _build_layout(self):
        root = ttk.Frame(self, padding=14)
        root.pack(fill="both", expand=True)

        top = ttk.Frame(root, style="Card.TFrame", padding=12)
        top.pack(fill="x", pady=(0, 10))

        ttk.Label(top, text="InstaPilot", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            top,
            text="Hesabının konusunu netleştir, içeriklerini takip et, keşfet trendlerinden müşteri çek.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        self.kpi_var = tk.StringVar(value="Hazır")
        ttk.Label(top, textvariable=self.kpi_var, style="Muted.TLabel").pack(anchor="e")

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        self.dashboard_tab = ttk.Frame(self.tabs, padding=14)
        self.content_tab = ttk.Frame(self.tabs, padding=14)
        self.explore_tab = ttk.Frame(self.tabs, padding=14)
        self.niche_tab = ttk.Frame(self.tabs, padding=14)
        self.strategy_tab = ttk.Frame(self.tabs, padding=14)

        self.tabs.add(self.dashboard_tab, text="Panel")
        self.tabs.add(self.content_tab, text="İçerik Kontrol")
        self.tabs.add(self.explore_tab, text="Keşfet Radar")
        self.tabs.add(self.niche_tab, text="Konu Tespiti")
        self.tabs.add(self.strategy_tab, text="Büyüme Planı")

        self._build_dashboard()
        self._build_content_tab()
        self._build_explore_tab()
        self._build_niche_tab()
        self._build_strategy_tab()

    def _card(self, parent, title):
        card = ttk.Frame(parent, style="Card.TFrame", padding=12)
        card.pack(fill="x", pady=(0, 10))
        ttk.Label(card, text=title, style="Header.TLabel").pack(anchor="w", pady=(0, 8))
        return card

    def _build_dashboard(self):
        card = self._card(self.dashboard_tab, "Hızlı Özet")
        self.summary_text = tk.Text(card, height=10, wrap="word", font=("Segoe UI", 10))
        self.summary_text.pack(fill="both", expand=True)
        self.summary_text.insert(
            "1.0",
            "• Konu tespitini tamamladıktan sonra net bir içerik omurgası oluşur.\n"
            "• İçerik Kontrol sekmesinden post fikirlerini ve hedeflerini kaydet.\n"
            "• Keşfet Radar ile trend formatları izleyip kendi nişine uyarlayabilirsin.\n"
            "• Büyüme Planı sekmesinde haftalık aksiyonları takip et.\n",
        )

    def _build_content_tab(self):
        form = self._card(self.content_tab, "Yeni İçerik Ekle")

        self.title_var = tk.StringVar()
        self.format_var = tk.StringVar(value="Reels")
        self.goal_var = tk.StringVar(value="Etkileşim")

        row1 = ttk.Frame(form)
        row1.pack(fill="x", pady=4)
        ttk.Label(row1, text="Başlık", width=18).pack(side="left")
        ttk.Entry(row1, textvariable=self.title_var).pack(side="left", fill="x", expand=True)

        row2 = ttk.Frame(form)
        row2.pack(fill="x", pady=4)
        ttk.Label(row2, text="Format", width=18).pack(side="left")
        ttk.Combobox(row2, textvariable=self.format_var, values=["Reels", "Carousel", "Story", "Canlı Yayın"], state="readonly").pack(side="left", fill="x", expand=True)

        row3 = ttk.Frame(form)
        row3.pack(fill="x", pady=4)
        ttk.Label(row3, text="Hedef", width=18).pack(side="left")
        ttk.Combobox(row3, textvariable=self.goal_var, values=["Etkileşim", "Takipçi", "DM", "Satış"], state="readonly").pack(side="left", fill="x", expand=True)

        ttk.Button(form, text="İçeriği Kaydet", command=self.add_content).pack(anchor="e", pady=(8, 0))

        list_card = self._card(self.content_tab, "Kayıtlı İçerikler")
        self.content_list = tk.Listbox(list_card, height=12, font=("Consolas", 10))
        self.content_list.pack(fill="both", expand=True)

    def _build_explore_tab(self):
        card = self._card(self.explore_tab, "Trend ve Keşfet Takibi")
        ttk.Label(card, text="Bugün keşfette hangi formatlar öne çıkıyor?", style="Muted.TLabel").pack(anchor="w")
        self.explore_box = tk.Text(card, height=16, wrap="word", font=("Segoe UI", 10))
        self.explore_box.pack(fill="both", expand=True, pady=(8, 0))
        self.explore_box.insert(
            "1.0",
            "1) 7-12 saniyelik hızlı Reels açılışları\n"
            "2) Önce problem sonra çözüm yaklaşımı\n"
            "3) Önce/sonra dönüşüm gösteren görseller\n"
            "4) Yorumlarda anahtar kelime isteyen CTA metinleri\n\n"
            "Not: Her trendi körü körüne kopyalamak yerine nişine uygunlaştır.",
        )

    def _build_niche_tab(self):
        card = self._card(self.niche_tab, "Sayfa Konusunu Netleştir")
        self.topic_var = tk.StringVar()
        self.audience_var = tk.StringVar()
        self.offer_var = tk.StringVar()
        self.style_var = tk.StringVar()

        fields = [
            ("Ana Konu", self.topic_var, "Örn: Yerel işletmeler için sosyal medya"),
            ("Hedef Kitle", self.audience_var, "Örn: 25-40 yaş girişimciler"),
            ("Ana Teklif", self.offer_var, "Örn: DM'den müşteri getiren içerik sistemi"),
            ("İletişim Stili", self.style_var, "Örn: Eğitici + samimi"),
        ]
        for label, var, hint in fields:
            row = ttk.Frame(card)
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=label, width=18).pack(side="left")
            entry = ttk.Entry(row, textvariable=var)
            entry.pack(side="left", fill="x", expand=True)
            ttk.Label(row, text=hint, style="Muted.TLabel").pack(side="left", padx=(10, 0))

        ttk.Button(card, text="Konu Analizi Yap", command=self.analyze_niche).pack(anchor="e", pady=(8, 0))

        self.niche_result = tk.Text(card, height=9, wrap="word", font=("Segoe UI", 10))
        self.niche_result.pack(fill="both", expand=True, pady=(8, 0))

    def _build_strategy_tab(self):
        card = self._card(self.strategy_tab, "Haftalık Büyüme Önerileri")
        self.strategy_text = tk.Text(card, height=20, wrap="word", font=("Segoe UI", 10))
        self.strategy_text.pack(fill="both", expand=True)
        self.strategy_text.insert(
            "1.0",
            "• Haftada 4 Reels + 2 Carousel üret.\n"
            "• Her içerikte tek bir CTA kullan: DM, yorum ya da bio tıklaması.\n"
            "• Haftada 2 kez nişindeki hesaplarla ortak yayın planla.\n"
            "• Her pazar performans analizi: izlenme, kaydetme, DM dönüşümü.\n",
        )

    def add_content(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Eksik Bilgi", "Lütfen içerik başlığı gir.")
            return

        item = {
            "title": title,
            "format": self.format_var.get(),
            "goal": self.goal_var.get(),
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        self.content_items.append(item)
        self._refresh_content_list()
        self.title_var.set("")
        self._save_state()

    def analyze_niche(self):
        profile = NicheProfile(
            topic=self.topic_var.get(),
            audience=self.audience_var.get(),
            offer=self.offer_var.get(),
            style=self.style_var.get(),
        )
        score = profile.score()
        clarity = "Net" if score >= 75 else "Geliştirilmeli"

        result = (
            f"Konu Netlik Skoru: {score}/100 ({clarity})\n\n"
            f"Ana Konu: {profile.topic or '-'}\n"
            f"Hedef Kitle: {profile.audience or '-'}\n"
            f"Ana Teklif: {profile.offer or '-'}\n"
            f"Stil: {profile.style or '-'}\n\n"
            "Öneri:\n"
        )

        if score < 50:
            result += "- Tek bir probleme odaklan ve teklifini ölçülebilir hale getir.\n"
        elif score < 75:
            result += "- Hedef kitleyi daralt (ör. herkes yerine belirli sektör).\n"
        else:
            result += "- Bu omurgayı 30 günlük içerik planına çevir ve tutarlı paylaş.\n"

        self.niche_result.delete("1.0", "end")
        self.niche_result.insert("1.0", result)
        self.last_profile = profile
        self.kpi_var.set(f"Konu netlik skoru güncellendi: {score}/100")
        self._save_state()

    def _refresh_content_list(self):
        self.content_list.delete(0, "end")
        for i, item in enumerate(self.content_items, start=1):
            self.content_list.insert(
                "end",
                f"{i:02d} | {item['created_at']} | {item['format']:<10} | {item['goal']:<10} | {item['title']}",
            )

    def _load_state(self):
        if not DATA_FILE.exists():
            return
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            self.content_items = data.get("content_items", [])
            profile = data.get("last_profile")
            if profile:
                self.topic_var.set(profile.get("topic", ""))
                self.audience_var.set(profile.get("audience", ""))
                self.offer_var.set(profile.get("offer", ""))
                self.style_var.set(profile.get("style", ""))
            self._refresh_content_list()
        except (json.JSONDecodeError, OSError):
            messagebox.showwarning("Uyarı", "Kayıt dosyası okunamadı.")

    def _save_state(self):
        payload = {
            "content_items": self.content_items,
            "last_profile": {
                "topic": self.topic_var.get(),
                "audience": self.audience_var.get(),
                "offer": self.offer_var.get(),
                "style": self.style_var.get(),
            },
        }
        DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    app = InstagramGrowthApp()
    app.mainloop()
