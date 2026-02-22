from __future__ import annotations

from typing import List, Optional

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.analytics import (
    calculate_engagement_rate,
    content_type_engagement,
    hourly_engagement,
    top_posts_by_engagement,
)
from app.instagram_api import InstagramAPIError, InstagramGraphClient
from app.models import FollowerPoint, InstagramPost
from app.token_store import TokenStore


class InstagramAnalyzerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Instagram Analiz Uygulaması")
        self.resize(1200, 800)

        self.token_store = TokenStore()
        self.posts: List[InstagramPost] = []
        self.follower_count: int = 0
        self.follower_growth: List[FollowerPoint] = []

        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.Password)
        self.user_id_input = QLineEdit()

        self.refresh_button = QPushButton("Verileri Güncelle")
        self.refresh_button.clicked.connect(self.refresh_data)

        self.general_stats_label = QLabel("Henüz veri yok")
        self.top_posts_table = QTableWidget()
        self.posts_table = QTableWidget()

        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)

        self._setup_ui()
        self._load_saved_token()

    def _setup_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)

        auth_box = QGroupBox("Instagram Graph API Bağlantısı")
        auth_layout = QFormLayout(auth_box)
        auth_layout.addRow("Access Token:", self.token_input)
        auth_layout.addRow("Instagram User ID:", self.user_id_input)
        auth_layout.addRow(self.refresh_button)

        tabs = QTabWidget()
        tabs.addTab(self._create_general_tab(), "Genel İstatistik")
        tabs.addTab(self._create_posts_tab(), "Gönderi Analizi")
        tabs.addTab(self._create_graphs_tab(), "Grafikler")

        layout.addWidget(auth_box)
        layout.addWidget(tabs)
        self.setCentralWidget(root)

    def _create_general_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.general_stats_label.setAlignment(Qt.AlignTop)
        layout.addWidget(self.general_stats_label)

        self.top_posts_table.setColumnCount(5)
        self.top_posts_table.setHorizontalHeaderLabels(
            ["Post ID", "Tür", "Beğeni", "Yorum", "Etkileşim Oranı"]
        )
        layout.addWidget(QLabel("En yüksek etkileşim alan gönderiler"))
        layout.addWidget(self.top_posts_table)
        return tab

    def _create_posts_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.posts_table.setColumnCount(6)
        self.posts_table.setHorizontalHeaderLabels(
            ["Post ID", "Tarih", "Tür", "Beğeni", "Yorum", "Etkileşim Oranı"]
        )
        layout.addWidget(self.posts_table)
        return tab

    def _create_graphs_tab(self) -> QWidget:
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(self.canvas, 0, 0)
        return tab

    def _load_saved_token(self) -> None:
        token_payload = self.token_store.load_token()
        if token_payload:
            self.token_input.setText(token_payload.get("access_token", ""))
            self.user_id_input.setText(token_payload.get("ig_user_id", ""))

    def refresh_data(self) -> None:
        access_token = self.token_input.text().strip()
        ig_user_id = self.user_id_input.text().strip()

        if not access_token or not ig_user_id:
            QMessageBox.warning(self, "Eksik Bilgi", "Token ve User ID gereklidir.")
            return

        try:
            self.token_store.save_token(access_token, ig_user_id)
            client = InstagramGraphClient(access_token, ig_user_id)

            profile = client.get_profile()
            self.follower_count = int(profile.get("followers_count", 0))
            self.posts = client.get_recent_posts(limit=50)
            self.follower_growth = client.get_follower_growth()

            self._update_general_stats(profile.get("username", "Bilinmiyor"))
            self._update_posts_table()
            self._update_top_posts_table()
            self._update_charts()

            QMessageBox.information(self, "Başarılı", "Veriler güncellendi.")
        except InstagramAPIError as exc:
            QMessageBox.critical(self, "API Hatası", str(exc))
        except Exception as exc:
            QMessageBox.critical(self, "Beklenmeyen Hata", str(exc))

    def _update_general_stats(self, username: str) -> None:
        avg_engagement = 0.0
        if self.posts:
            avg_engagement = sum(
                calculate_engagement_rate(post, self.follower_count) for post in self.posts
            ) / len(self.posts)

        summary = (
            f"Kullanıcı: @{username}\n"
            f"Takipçi Sayısı: {self.follower_count}\n"
            f"İncelenen Gönderi Sayısı: {len(self.posts)}\n"
            f"Ortalama Etkileşim Oranı: %{avg_engagement * 100:.2f}"
        )
        self.general_stats_label.setText(summary)

    def _update_posts_table(self) -> None:
        self.posts_table.setRowCount(len(self.posts))

        for row, post in enumerate(self.posts):
            engagement = calculate_engagement_rate(post, self.follower_count) * 100
            values = [
                post.post_id,
                post.timestamp.strftime("%Y-%m-%d %H:%M"),
                post.content_type,
                str(post.like_count),
                str(post.comments_count),
                f"%{engagement:.2f}",
            ]
            for col, value in enumerate(values):
                self.posts_table.setItem(row, col, QTableWidgetItem(value))

        self.posts_table.resizeColumnsToContents()

    def _update_top_posts_table(self) -> None:
        ranked = top_posts_by_engagement(self.posts, self.follower_count, top_n=10)
        self.top_posts_table.setRowCount(len(ranked))

        for row, (post, rate) in enumerate(ranked):
            values = [
                post.post_id,
                post.content_type,
                str(post.like_count),
                str(post.comments_count),
                f"%{rate * 100:.2f}",
            ]
            for col, value in enumerate(values):
                self.top_posts_table.setItem(row, col, QTableWidgetItem(value))

        self.top_posts_table.resizeColumnsToContents()

    def _update_charts(self) -> None:
        self.figure.clear()

        ax1 = self.figure.add_subplot(221)
        ax2 = self.figure.add_subplot(222)
        ax3 = self.figure.add_subplot(212)

        hourly = hourly_engagement(self.posts, self.follower_count)
        ax1.bar(list(hourly.keys()), [val * 100 for val in hourly.values()], color="#4e79a7")
        ax1.set_title("Saat Bazlı Ortalama Etkileşim (%)")
        ax1.set_xlabel("Saat")
        ax1.set_ylabel("Etkileşim %")

        by_type = content_type_engagement(self.posts, self.follower_count)
        ax2.bar(list(by_type.keys()), [val * 100 for val in by_type.values()], color="#59a14f")
        ax2.set_title("İçerik Türüne Göre Ortalama Etkileşim (%)")
        ax2.set_ylabel("Etkileşim %")

        if self.follower_growth:
            dates = [p.date for p in self.follower_growth]
            counts = [p.follower_count for p in self.follower_growth]
            ax3.plot(dates, counts, marker="o", color="#f28e2b")
            ax3.set_title("Takipçi Artış Grafiği")
            ax3.set_xlabel("Tarih")
            ax3.set_ylabel("Takipçi")
        else:
            ax3.text(0.5, 0.5, "Takipçi artış verisi bulunamadı", ha="center", va="center")
            ax3.set_axis_off()

        self.figure.tight_layout()
        self.canvas.draw()


def run_app() -> None:
    app = QApplication([])
    window = InstagramAnalyzerWindow()
    window.show()
    app.exec_()
