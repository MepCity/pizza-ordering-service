# ruff: noqa: E501

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image as RLImage
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def get_font(size: int, bold: bool = False):
    arial_font = (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf"
    )
    candidates = [
        arial_font,
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def draw_box(draw: ImageDraw.ImageDraw, xy, text: str, fill: str, outline: str = "#1f2937"):
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=outline, width=3)
    font = get_font(28, bold=True)
    text_bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=6, align="center")
    tw = text_bbox[2] - text_bbox[0]
    th = text_bbox[3] - text_bbox[1]
    x1, y1, x2, y2 = xy
    tx = x1 + ((x2 - x1) - tw) / 2
    ty = y1 + ((y2 - y1) - th) / 2
    draw.multiline_text((tx, ty), text, font=font, fill="#111827", spacing=6, align="center")


def draw_arrow(draw: ImageDraw.ImageDraw, start, end, color="#374151"):
    draw.line([start, end], fill=color, width=5)
    ex, ey = end
    sx, sy = start
    if abs(ex - sx) >= abs(ey - sy):
        direction = 1 if ex > sx else -1
        draw.polygon(
            [(ex, ey), (ex - 18 * direction, ey - 10), (ex - 18 * direction, ey + 10)],
            fill=color,
        )
    else:
        direction = 1 if ey > sy else -1
        draw.polygon(
            [(ex, ey), (ex - 10, ey - 18 * direction), (ex + 10, ey - 18 * direction)],
            fill=color,
        )


def generate_architecture_png() -> None:
    image = Image.new("RGB", (1600, 900), "#f8fafc")
    draw = ImageDraw.Draw(image)
    title_font = get_font(40, bold=True)
    draw.text((60, 40), "Pizza Ordering Service Architecture", font=title_font, fill="#0f172a")

    boxes = {
        "clients": (70, 180, 360, 320),
        "api": (500, 180, 840, 340),
        "db": (1040, 120, 1450, 240),
        "s3": (1040, 290, 1450, 410),
        "prom": (500, 470, 840, 590),
        "grafana": (1040, 470, 1450, 590),
        "ci": (70, 500, 360, 680),
        "k8s": (500, 680, 840, 820),
    }

    draw_box(draw, boxes["clients"], "Web UI\nPostman\nk6 / Playwright", "#dbeafe")
    draw_box(draw, boxes["api"], "FastAPI Service\n/menu, /orders, /metrics", "#dcfce7")
    draw_box(draw, boxes["db"], "PostgreSQL /\nSQLite", "#fde68a")
    draw_box(draw, boxes["s3"], "LocalStack S3\nOrder Archive", "#fecaca")
    draw_box(draw, boxes["prom"], "Prometheus\nMetrics Scrape", "#e9d5ff")
    draw_box(draw, boxes["grafana"], "Grafana\nDashboards", "#fbcfe8")
    draw_box(draw, boxes["ci"], "GitHub Actions\nLint + Pytest + Newman\nDocker Build + Smoke", "#fed7aa")
    draw_box(draw, boxes["k8s"], "Docker Compose /\nKubernetes / Minikube", "#bfdbfe")

    draw_arrow(draw, (360, 250), (500, 250))
    draw_arrow(draw, (840, 220), (1040, 180))
    draw_arrow(draw, (840, 320), (1040, 350))
    draw_arrow(draw, (670, 340), (670, 470))
    draw_arrow(draw, (840, 530), (1040, 530))
    draw_arrow(draw, (360, 590), (500, 590))
    draw_arrow(draw, (670, 680), (670, 590))

    image.save(DOCS / "architecture.png")


def report_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            textColor=colors.HexColor("#111827"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ReportHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles["BodyText"].fontName = "Helvetica"
    styles["BodyText"].fontSize = 10.5
    styles["BodyText"].leading = 15
    return styles


def build_report_pdf() -> None:
    styles = report_styles()
    story = [
        Paragraph("Pizza Ordering Service Final Raporu", styles["ReportTitle"]),
        Paragraph(
            "Bu proje, küçük bir pizza sipariş domain’i üzerinden test mühendisliği, CI/CD, container, gözlemlenebilirlik ve dağıtım pratiklerini bir araya getiren bir backend uygulaması olarak geliştirilmiştir.",
            styles["BodyText"],
        ),
        Spacer(1, 0.4 * cm),
        RLImage(str(DOCS / "architecture.png"), width=16 * cm, height=9 * cm),
        Spacer(1, 0.4 * cm),
    ]

    first_page_sections = [
        (
            "1. Giriş",
            [
                "Projenin temel hedefi karmaşık bir iş alanı modellemek değil, sınırlı kapsamlı bir servis etrafında endüstri standardına yakın bir teslim süreci oluşturmaktır.",
                "Bu kapsamda FastAPI ile REST servis geliştirilmiş, siparişlerin veritabanında tutulması, LocalStack S3 üzerinde arşivlenmesi ve test altyapısıyla doğrulanması sağlanmıştır.",
            ],
        ),
    ]
    second_page_sections = [
        (
            "2. Mimari Bileşenler",
            [
                "Sistem FastAPI tabanlı bir uygulama, PostgreSQL veya SQLite veritabanı, LocalStack S3, Prometheus ve Grafana bileşenlerinden oluşmaktadır.",
                "GitHub Actions, lint, test, Docker build, Newman ve smoke test adımlarını çalıştırarak CI hattını oluşturmaktadır.",
                "Yerel geliştirme için Docker Compose kullanılmış, dağıtım hedefi olarak ise Kubernetes manifestleri hazırlanmıştır.",
            ],
        ),
        (
            "3. Test Stratejisi",
            [
                "Unit testler fiyat hesaplama, kupon uygulama, durum geçişleri ve API davranışını doğrulamaktadır.",
                "Integration testler PostgreSQL ve LocalStack üzerinden gerçek persistence ve arşivleme davranışını kontrol etmektedir.",
                "Playwright için temel E2E omurgası hazırlanmış, kısıtlı ortamlarda suite'i kırmadan skip olacak şekilde düzenlenmiştir.",
                "Postman ve Newman koleksiyonu ile endpoint sıralı doğrulama yapılmakta, coverage eşiği CI tarafında en az yüzde 70 olarak zorunlu tutulmaktadır.",
            ],
        ),
    ]
    third_page_sections = [
        (
            "4. API Kapsamı ve Teknik Çıktılar",
            [
                "Serviste sağlık kontrolü, menü listeleme, sipariş oluşturma, sipariş listeleme, sipariş detayı görüntüleme, sipariş durumu güncelleme ve kupon uygulama uçları yer almaktadır.",
                "Factory Boy ve Faker ile test verisi üretimi için `MenuItemFactory`, `OrderItemFactory` ve `OrderFactory` tanımlanmıştır.",
                "Kubernetes tarafında Deployment, Service, ConfigMap ve Secret dosyaları hazırlanmış, Dockerfile multi-stage olarak kurgulanmıştır.",
            ],
        ),
        (
            "5. Pipeline ve Dağıtım",
            [
                "CI hattında ruff lint kontrolü, pytest coverage kontrolü, Docker image build, smoke test ve Newman koleksiyonu çalıştırılmaktadır.",
                "Kubernetes tarafında Deployment, Service, ConfigMap ve Secret dosyaları hazırlanmıştır. Docker Compose ile yerel ortamda PostgreSQL, LocalStack, Prometheus ve Grafana birlikte ayağa kaldırılabilmektedir.",
                "Yerel raporlama için mimari PNG, final rapor PDF ve slayt PDF çıktıları otomatik üretilmiştir.",
            ],
        ),
        (
            "6. Performans ve Gözlemlenebilirlik",
            [
                "Prometheus uygulamanın `/metrics` endpoint'ini scrape etmektedir. Grafana dashboard'unda throughput, error rate ve p95 latency panelleri tanımlıdır.",
                "Yük testi akışı `GET /menu`, `POST /orders` ve `PATCH /orders/{id}/status` uçlarını hedeflemektedir.",
                "Yerel Locust ölçümünde p95 latency 16 ms, maksimum gecikme 30 ms ve hata oranı yüzde 0 olarak gözlemlenmiştir.",
                "Toplam 66 isteklik ölçümde ortalama gecikme 7 ms ve throughput değeri 4.63 req/s olarak kaydedilmiştir.",
            ],
        ),
    ]
    fourth_page_sections = [
        (
            "7. Karşılaşılan Zorluklar ve Öğrenilenler",
            [
                "En önemli teknik öğrenimlerden biri Testcontainers ile kullanılan PostgreSQL sürücüsünün projedeki `psycopg` bağımlılığıyla hizalanması olmuştur.",
                "Ayrıca ortama bağlı testlerin kontrollü skip edilmesi, gözlemlenebilirlik dosyalarının erken hazırlanması ve Kubernetes secret ayrımı proje kalitesini artırmıştır.",
                "Playwright ve performans testlerinde bazı ortamlarda port ve browser erişimi kısıtlı olabildiği için testler gerektiğinde güvenli şekilde skip olacak biçimde tasarlanmıştır.",
            ],
        ),
        (
            "8. Sonuç",
            [
                "Proje, şartnamedeki mini servis, test, container, LocalStack, veritabanı, monitoring ve performans katmanlarının büyük bölümünü tamamlamış durumdadır.",
                "Özellikle CI entegrasyonu, arşivleme davranışı, ölçümleme altyapısı ve teslimat dosyalarının otomatik üretilmesi projeyi sunuma hazır hale getirmiştir.",
            ],
        ),
        (
            "9. Kaynaklar",
            [
                "FastAPI, SQLAlchemy, Testcontainers, LocalStack, Prometheus, Grafana ve k6 dokümantasyonları proje boyunca başlıca referanslar olarak kullanılmıştır.",
            ],
        ),
    ]

    all_section_groups = [
        first_page_sections,
        second_page_sections,
        third_page_sections,
        fourth_page_sections,
    ]

    for group_index, sections in enumerate(all_section_groups):
        for heading, paragraphs in sections:
            story.append(Spacer(1, 0.2 * cm))
            story.append(Paragraph(heading, styles["ReportHeading"]))
            for paragraph in paragraphs:
                story.append(Paragraph(paragraph, styles["BodyText"]))
                story.append(Spacer(1, 0.15 * cm))
        if group_index < len(all_section_groups) - 1:
            story.append(PageBreak())

    doc = SimpleDocTemplate(
        str(DOCS / "final-report.pdf"),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
    )
    doc.build(story)


def build_slides_pdf() -> None:
    styles = report_styles()
    slides = [
        ("Pizza Ordering Service", ["Bulut mimarilerinde test mühendisliği dönem projesi", "FastAPI, PostgreSQL, LocalStack, Docker, Kubernetes"]),
        ("Problem ve Kapsam", ["Küçük ama savunulabilir bir domain seçildi", "Amaç: test, CI/CD ve gözlemlenebilirlik altyapısı kurmak", "Ödeme ve kimlik doğrulama bilinçli olarak kapsam dışında bırakıldı"]),
        ("Mimari", ["FastAPI servis katmanı", "PostgreSQL / SQLite persistence", "LocalStack S3 arşivleme", "Prometheus + Grafana monitoring"]),
        ("API ve İş Kuralları", ["Menu listeleme", "Sipariş oluşturma", "Durum geçişleri: pending -> preparing -> ready -> delivered", "Kupon ve extra doğrulama"]),
        ("Test Stratejisi", ["Unit testler", "PostgreSQL integration testler", "LocalStack integration testler", "Postman/Newman koleksiyonu", "Playwright E2E iskeleti"]),
        ("CI/CD ve Dağıtım", ["GitHub Actions: lint + pytest + Newman + smoke", "Docker Compose ile lokal ortam", "Kubernetes Deployment, Service, ConfigMap, Secret"]),
        ("Monitoring ve Performans", ["Grafana panelleri: throughput, error rate, p95 latency", "Yük testi akışı: menu + order + status update", "Örnek Locust sonucu: p95 16 ms, hata oranı yüzde 0"]),
    ]

    story = []
    for index, (title, bullets) in enumerate(slides):
        story.append(Paragraph(title, styles["ReportTitle"]))
        story.append(Spacer(1, 0.8 * cm))
        for bullet in bullets:
            story.append(Paragraph(f"• {bullet}", styles["BodyText"]))
            story.append(Spacer(1, 0.35 * cm))
        if index < len(slides) - 1:
            story.append(PageBreak())

    doc = SimpleDocTemplate(
        str(DOCS / "slides.pdf"),
        pagesize=landscape(A4),
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
    )
    doc.build(story)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    generate_architecture_png()
    build_report_pdf()
    build_slides_pdf()


if __name__ == "__main__":
    main()
