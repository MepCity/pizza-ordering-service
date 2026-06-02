from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph, Frame, Spacer
from reportlab.lib.styles import ParagraphStyle

pdfmetrics.registerFont(TTFont("Arial",        "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold",   "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", "C:/Windows/Fonts/ariali.ttf"))

W, H = 33.87*cm, 19.05*cm   # 16:9 sunum boyutu

DARK   = colors.HexColor("#1a1a2e")
BLUE   = colors.HexColor("#0f3460")
ACCENT = colors.HexColor("#e94560")
LIGHT  = colors.HexColor("#f0f4f8")
WHITE  = colors.white
GRAY   = colors.HexColor("#555555")
LGRAY  = colors.HexColor("#cccccc")

OUTPUT = "docs/slides.pdf"
c = canvas.Canvas(OUTPUT, pagesize=(W, H))

def ps(name, font="Arial", size=11, color=colors.black, leading=None, align=0):
    return ParagraphStyle(name, fontName=font, fontSize=size,
                          textColor=color, leading=leading or size*1.3,
                          alignment=align)

# ─── Yardımcı çizim fonksiyonları ────────────────────────────────────────

def bg(color=WHITE):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def header_bar(title, subtitle=None, tag=None):
    # Üst koyu şerit
    c.setFillColor(DARK)
    c.rect(0, H - 3.6*cm, W, 3.6*cm, fill=1, stroke=0)
    # Accent çizgi
    c.setFillColor(ACCENT)
    c.rect(0, H - 3.6*cm - 0.18*cm, W, 0.18*cm, fill=1, stroke=0)
    # Başlık
    c.setFont("Arial-Bold", 22)
    c.setFillColor(WHITE)
    c.drawString(1.2*cm, H - 2.2*cm, title)
    if subtitle:
        c.setFont("Arial", 11)
        c.setFillColor(colors.HexColor("#aaaaaa"))
        c.drawString(1.2*cm, H - 3.1*cm, subtitle)
    if tag:
        c.setFont("Arial-Italic", 9)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawRightString(W - 1.2*cm, H - 3.1*cm, tag)

def footer(page_no, total=9):
    c.setFillColor(DARK)
    c.rect(0, 0, W, 0.7*cm, fill=1, stroke=0)
    c.setFont("Arial", 8)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawString(1.2*cm, 0.22*cm, "Pizza Ordering Service  |  Bulut Mimarilerinde Test Mühendisliği  |  MTH2526-B25")
    c.drawRightString(W - 1.2*cm, 0.22*cm, f"{page_no} / {total}")

def bullet_list(items, x, y, w, size=11, gap=0.5*cm):
    style = ps("b", size=size, leading=size*1.4)
    for item in items:
        p = Paragraph(f"<bullet>&bull;</bullet>  {item}", style)
        p.wrapOn(c, w, 5*cm)
        p.drawOn(c, x, y - p.height)
        y -= p.height + gap
    return y

def draw_table(data, col_widths, x, y, header_color=DARK, font_size=9):
    style = [
        ("BACKGROUND",    (0,0), (-1,0),  header_color),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Arial-Bold"),
        ("FONTNAME",      (0,1), (-1,-1), "Arial"),
        ("FONTSIZE",      (0,0), (-1,-1), font_size),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [LIGHT, WHITE]),
        ("GRID",          (0,0), (-1,-1), 0.3, LGRAY),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]
    ps_cell = ps("cell", size=font_size, leading=font_size*1.3)
    para_data = []
    for row in data:
        para_row = []
        for cell in row:
            para_row.append(Paragraph(str(cell), ps_cell))
        para_data.append(para_row)
    t = Table(para_data, colWidths=col_widths)
    t.setStyle(TableStyle(style))
    tw, th = t.wrapOn(c, sum(col_widths), 50*cm)
    t.drawOn(c, x, y - th)
    return y - th

TOTAL = 9

# ═══════════════════════════════════════════════════════════════════════════
# SLAYT 1 — KAPAK
# ═══════════════════════════════════════════════════════════════════════════
bg(DARK)
# Dekoratif daire
c.setFillColor(BLUE)
c.circle(W - 4*cm, H/2, 5.5*cm, fill=1, stroke=0)
c.setFillColor(ACCENT)
c.circle(W - 4*cm, H/2, 2*cm, fill=1, stroke=0)

c.setFillColor(WHITE)
c.setFont("Arial-Bold", 36)
c.drawString(1.8*cm, H/2 + 3*cm, "Pizza Ordering Service")
c.setFont("Arial", 16)
c.setFillColor(colors.HexColor("#aaaaaa"))
c.drawString(1.8*cm, H/2 + 1.8*cm, "Dönem Projesi Final Sunumu")
c.setFillColor(ACCENT)
c.rect(1.8*cm, H/2 + 1.4*cm, 8*cm, 0.12*cm, fill=1, stroke=0)
c.setFont("Arial", 12)
c.setFillColor(colors.HexColor("#cccccc"))
c.drawString(1.8*cm, H/2 + 0.7*cm, "Bulut Mimarilerinde Test Mühendisliği  |  MTH2526-B25")
c.drawString(1.8*cm, H/2 - 0.1*cm, "Marmara Üniversitesi — Bilgisayar Mühendisliği")
c.setFont("Arial-Bold", 11)
c.setFillColor(WHITE)
c.drawString(1.8*cm, H/2 - 1.2*cm, "Yasir ARSLAN — 170423528")
c.drawString(1.8*cm, H/2 - 1.9*cm, "Büşra Ecem ÖZBEK — 170423966")
c.setFont("Arial", 10)
c.setFillColor(colors.HexColor("#888888"))
c.drawString(1.8*cm, H/2 - 2.7*cm, "Haziran 2026")
footer(1, TOTAL)
c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# SLAYT 2 — PROJE HAKKINDA
# ═══════════════════════════════════════════════════════════════════════════
bg()
header_bar("Proje Hakkında", "Ne yaptık? Neden pizza?")
footer(2, TOTAL)

c.setFont("Arial-Bold", 13)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 5*cm, "Amaç")

bullet_list([
    "Karmaşık uygulama değil — <b>endüstri standardında test ve dağıtım altyapısı</b> kurmak.",
    "Domain: pizza siparişi — basit ama test edilebilir iş kuralları zengin.",
    "Bilinçli kapsam dışı: ödeme sistemi, kimlik doğrulama.",
], 1.2*cm, H - 5.8*cm, 14*cm, size=12)

c.setFont("Arial-Bold", 13)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 9.5*cm, "Teknoloji Yığını")

tech_data = [
    ["Katman", "Teknoloji"],
    ["API", "FastAPI + Python 3.12"],
    ["Veritabanı", "SQLAlchemy + PostgreSQL 16"],
    ["AWS Emülasyon", "LocalStack S3"],
    ["Monitoring", "Prometheus + Grafana"],
    ["Tracing", "OpenTelemetry + Jaeger"],
    ["Konteyner", "Docker Compose (7 servis)"],
    ["Kubernetes", "kind + KEDA + ArgoCD + Helm"],
]
draw_table(tech_data, [5*cm, 9*cm], 1.2*cm, H - 10.2*cm)

c.setFont("Arial-Bold", 13)
c.setFillColor(DARK)
c.drawString(17*cm, H - 5*cm, "Öne Çıkan İş Kuralları")
bullet_list([
    "Durum makinesi: pending → preparing → ready → delivered",
    "Extra malzeme: her extra +$2.50 (5 desteklenen)",
    "Kupon: PIZZA10 (%10), CHEESE20 (%20)",
    "Aynı siparişe 2. kupon uygulanamaz",
    "Durum atlaması engellenir (pending→delivered = hata)",
], 17*cm, H - 5.8*cm, 14.5*cm, size=11)
c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# SLAYT 3 — MİMARİ DİYAGRAM
# ═══════════════════════════════════════════════════════════════════════════
bg()
header_bar("Mimari", "Sistem bileşenleri ve aralarındaki ilişkiler")
footer(3, TOTAL)

# Sol sütun — servisler kutuları
boxes = [
    ("Tarayıcı / Postman", 1.2*cm, H - 6*cm, BLUE),
    ("FastAPI App", 1.2*cm, H - 8.2*cm, DARK),
    ("PostgreSQL 16", 1.2*cm, H - 10.4*cm, colors.HexColor("#336791")),
    ("LocalStack S3", 1.2*cm, H - 12.6*cm, colors.HexColor("#ff9900")),
]
for label, bx, by, bc in boxes:
    c.setFillColor(bc)
    c.roundRect(bx, by, 5.5*cm, 1.4*cm, 0.3*cm, fill=1, stroke=0)
    c.setFont("Arial-Bold", 10)
    c.setFillColor(WHITE)
    c.drawCentredString(bx + 2.75*cm, by + 0.5*cm, label)

# Oklar
c.setStrokeColor(DARK)
c.setLineWidth(1.2)
for y_from, y_to in [(H-4.6*cm, H-5.95*cm), (H-6*cm+1.4*cm-1.4*cm, H-8.1*cm),
                     (H-8.2*cm+1.4*cm-1.4*cm, H-10.3*cm), (H-10.4*cm+1.4*cm-1.4*cm, H-12.5*cm)]:
    pass
# Basit ok çizgileri
arrow_x = 1.2*cm + 2.75*cm
for y_start, y_end in [
    (H-5*cm, H-5*cm-1.2*cm),
    (H-7.2*cm, H-7.2*cm-1.2*cm),
    (H-9.4*cm, H-9.4*cm-1.2*cm),
]:
    c.setStrokeColor(GRAY)
    c.setLineWidth(1)
    c.line(arrow_x, y_start, arrow_x, y_end)
    # Ok ucu
    c.setFillColor(GRAY)
    c.triangle(arrow_x-0.2*cm, y_end+0.3*cm, arrow_x+0.2*cm, y_end+0.3*cm, arrow_x, y_end, fill=1, stroke=0) if hasattr(c, 'triangle') else None

# Sağ sütun — monitoring
c.setFont("Arial-Bold", 11)
c.setFillColor(DARK)
c.drawString(9*cm, H - 5*cm, "Monitoring & Observability")

mon_boxes = [
    ("Prometheus", colors.HexColor("#e6522c")),
    ("Grafana", colors.HexColor("#f46800")),
    ("Jaeger (OTel)", colors.HexColor("#60d0e4")),
]
mx = 9*cm
for i, (label, bc) in enumerate(mon_boxes):
    by2 = H - 6*cm - i*2.2*cm
    c.setFillColor(bc)
    c.roundRect(mx, by2, 5*cm, 1.4*cm, 0.3*cm, fill=1, stroke=0)
    c.setFont("Arial-Bold", 10)
    c.setFillColor(WHITE)
    c.drawCentredString(mx + 2.5*cm, by2 + 0.5*cm, label)

# K8s
c.setFont("Arial-Bold", 11)
c.setFillColor(DARK)
c.drawString(17*cm, H - 5*cm, "Kubernetes & CI/CD")

k8s_boxes = [
    ("GitHub Actions CI/CD", DARK),
    ("Kubernetes (kind)", colors.HexColor("#326ce5")),
    ("KEDA Autoscaling", colors.HexColor("#ff6b6b")),
    ("ArgoCD GitOps", colors.HexColor("#ef7b4d")),
    ("Helm Chart", colors.HexColor("#0f1689")),
]
for i, (label, bc) in enumerate(k8s_boxes):
    by3 = H - 6*cm - i*1.9*cm
    c.setFillColor(bc)
    c.roundRect(17*cm, by3, 6*cm, 1.3*cm, 0.3*cm, fill=1, stroke=0)
    c.setFont("Arial-Bold", 9)
    c.setFillColor(WHITE)
    c.drawCentredString(20*cm, by3 + 0.45*cm, label)

c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# SLAYT 4 — API ENDPOİNTLER
# ═══════════════════════════════════════════════════════════════════════════
bg()
header_bar("API Endpoint'leri", "7 REST endpoint — iş kurallarıyla")
footer(4, TOTAL)

api_data = [
    ["Method", "Endpoint", "Açıklama", "Önemli Kural"],
    ["GET",   "/health",                    "Sağlık kontrolü",        "CI smoke test + K8s probe"],
    ["GET",   "/menu",                      "Aktif menü listesi",     "is_available=True olanlar"],
    ["POST",  "/orders",                    "Sipariş oluştur",        "Fiyat hesabı + S3 arşivleme"],
    ["GET",   "/orders",                    "Tüm siparişler",         "Yeniden eskiye sıralı"],
    ["GET",   "/orders/{id}",               "Sipariş detayı",         "Bulunamazsa 404"],
    ["PATCH", "/orders/{id}/status",        "Durum güncelle",         "pending→preparing→ready→delivered"],
    ["POST",  "/orders/{id}/apply-coupon",  "Kupon uygula",           "İkinci kupon 400 hata"],
]
draw_table(api_data, [2.5*cm, 6*cm, 6*cm, 10*cm], 1.2*cm, H-4.8*cm, font_size=10)

c.setFont("Arial-Bold", 11)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 13.5*cm, "Fiyatlandırma Formülü")
c.setFont("Arial", 11)
c.setFillColor(GRAY)
c.drawString(1.2*cm, H - 14.3*cm, "Toplam = (Birim Fiyat × Adet) + (2.50 × Extra Sayısı × Adet)")
c.setFont("Arial-Italic", 10)
c.drawString(1.2*cm, H - 15*cm, "Örnek: Margherita medium ($11.99) × 4 adet + olive extra × 4 = $57.96")

c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# SLAYT 5 — TEST STRATEJİSİ
# ═══════════════════════════════════════════════════════════════════════════
bg()
header_bar("Test Stratejisi", "18 test — %86 coverage — test piramidi")
footer(5, TOTAL)

# Piramit çizimi
pyramid_x = 24*cm
pyramid_y = H - 5*cm
levels = [
    (5*cm, 1.5*cm, colors.HexColor("#c0392b"), "E2E (4)"),
    (8*cm, 1.5*cm, colors.HexColor("#e67e22"), "Integration (3)"),
    (11*cm, 1.5*cm, colors.HexColor("#27ae60"), "Unit (11)"),
]
base_x = pyramid_x - 5.5*cm
cur_y = pyramid_y
for w, h2, col, label in levels:
    bx = pyramid_x - w/2
    c.setFillColor(col)
    c.rect(bx, cur_y - h2, w, h2, fill=1, stroke=0)
    c.setFont("Arial-Bold", 9)
    c.setFillColor(WHITE)
    c.drawCentredString(pyramid_x, cur_y - h2/2 - 0.1*cm, label)
    cur_y -= h2

c.setFont("Arial-Bold", 11)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 4.8*cm, "Unit Testler — 11 adet")
c.setFillColor(colors.HexColor("#27ae60"))
c.rect(1.2*cm, H-5*cm, 0.3*cm, 0.3*cm, fill=1, stroke=0)

bullet_list([
    "SQLite in-memory — dış bağımlılık yok, 0.30 sn",
    "Geçersiz extra (pineapple) → 422",
    "Durum atlaması (pending→delivered) → 400",
    "Çift kupon → 400",
    "Sıralı durum geçişi doğrulaması",
    "S3 arşivleme tetiklenme kontrolü",
], 1.2*cm, H - 5.4*cm, 14*cm, size=10, gap=0.35*cm)

c.setFont("Arial-Bold", 11)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 10.5*cm, "Integration Testler — 3 adet")
bullet_list([
    "Testcontainers: gerçek PostgreSQL 16 + LocalStack S3",
    "Sipariş DB'ye yazılıyor mu? Fiyat doğru mu?",
    "Kupon sonrası total_price güncellendi mi?",
    "S3'te orders/{id}.json oluştu mu?",
], 1.2*cm, H - 11.2*cm, 14*cm, size=10, gap=0.35*cm)

c.setFont("Arial-Bold", 11)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 14.2*cm, "E2E Testler — 4 adet (Playwright Chromium)")
bullet_list([
    "Gerçek tarayıcı — form doldur, sipariş oluştur",
    "Sipariş listele ve detay görüntüle",
    "Geçersiz extra → hata mesajı sayfada görünsün",
], 1.2*cm, H - 14.9*cm, 14*cm, size=10, gap=0.35*cm)

c.setFont("Arial-Bold", 13)
c.setFillColor(ACCENT)
c.drawString(17.5*cm, H - 13*cm, "Coverage: %86")
c.setFont("Arial", 10)
c.setFillColor(GRAY)
c.drawString(17.5*cm, H - 13.8*cm, "(Şart: %70)")

c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# SLAYT 6 — CI/CD PİPELİNE
# ═══════════════════════════════════════════════════════════════════════════
bg()
header_bar("CI/CD Pipeline", "GitHub Actions — 13 adım — her push'ta tetiklenir")
footer(6, TOTAL)

pipeline_data = [
    ["Adım", "İşlem", "Araç"],
    ["1–4",  "Checkout → Python 3.11 → Node.js → kubectl → kind cluster", "GitHub Actions"],
    ["5–6",  "Bağımlılıklar + Playwright Chromium kurulum", "pip + playwright"],
    ["7",    "Lint kontrolü", "ruff check ."],
    ["8",    "Testler + Coverage kontrolü", "pytest --cov-fail-under=70"],
    ["9–10", "Docker image build + kind'a yükle", "docker build + kind load"],
    ["11–12","kubectl apply + rollout status bekleme (120s)", "kubectl"],
    ["13",   "Smoke test (curl /health) + Postman/Newman", "curl + newman run"],
]
draw_table(pipeline_data, [2*cm, 16*cm, 6*cm], 1.2*cm, H - 4.8*cm, font_size=10)

c.setFont("Arial-Bold", 12)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 13*cm, "Bonus Katmanlar (+20 puan)")

bonus_data = [
    ["Bonus", "Açıklama", "Puan"],
    ["Helm Chart",      "K8s kaynakları paketlendi, values.yaml merkezi yönetim",               "+5"],
    ["KEDA",            "Prometheus metriğine göre 1–5 replica otomatik ölçekleme",              "+5"],
    ["ArgoCD",          "main branch merge → otomatik cluster deploy (GitOps)",                  "+5"],
    ["OpenTelemetry",   "FastAPI + SQL + AWS uçtan uca tracing — Jaeger'da görünür",             "+5"],
]
draw_table(bonus_data, [4*cm, 16*cm, 2.5*cm], 1.2*cm, H - 13.7*cm, header_color=ACCENT, font_size=10)

c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# SLAYT 7 — MONİTORİNG VE PERFORMANS
# ═══════════════════════════════════════════════════════════════════════════
bg()
header_bar("Monitoring ve Performans", "Prometheus + Grafana + OpenTelemetry + Locust/k6")
footer(7, TOTAL)

c.setFont("Arial-Bold", 12)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 4.8*cm, "Grafana Dashboard — 3 Panel")

panel_data = [
    ["Panel", "Metrik", "Ne Gösterir?"],
    ["Request Throughput", "rate(http_requests_total[1m])", "Saniyedeki istek sayısı — trafik yoğunluğu"],
    ["Error Rate",         "rate(http_requests_total{status=~'5..'}[1m])", "HTTP 5xx oranı — sistem sağlığı"],
    ["Latency P95",        "histogram_quantile(0.95, http_request_duration)", "İsteklerin %95'inin yanıt süresi"],
]
draw_table(panel_data, [5*cm, 9*cm, 10.5*cm], 1.2*cm, H - 5.5*cm, font_size=10)

c.setFont("Arial-Bold", 12)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 9.5*cm, "Performans Testi")
bullet_list([
    "k6 (perf/load-test.js) ve Locust (perf/locustfile.py) ile yük testi.",
    "Senaryo: /menu + POST /orders + GET /orders eş zamanlı yük.",
    "p95 latency ölçümü — sonuçlar perf/report.md'de.",
], 1.2*cm, H - 10.2*cm, 15*cm, size=11)

c.setFont("Arial-Bold", 12)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 13*cm, "OpenTelemetry Distributed Tracing")
bullet_list([
    "FastAPI istekleri, SQLAlchemy sorguları ve S3 çağrıları otomatik trace edilir.",
    "Trace'ler Jaeger UI'da görüntülenebilir — localhost:16686.",
    "Bir isteğin API'den DB'ye, S3'e kadar tüm süreci tek ekranda takip edilir.",
], 1.2*cm, H - 13.7*cm, 25*cm, size=11)

c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# SLAYT 8 — SAYILAR VE ÖĞRENDİKLERİMİZ
# ═══════════════════════════════════════════════════════════════════════════
bg()
header_bar("Sayılar ve Öğrendiklerimiz", "Proje özeti")
footer(8, TOTAL)

# Sol — sayılar kutuları
metrics = [
    ("18", "Test"),
    ("%86", "Coverage"),
    ("7", "Endpoint"),
    ("7", "Docker Servis"),
    ("13", "CI Adımı"),
    ("+20", "Bonus Puan"),
]
cols = 3
box_w = 7*cm
box_h = 2.8*cm
start_x = 0.8*cm
start_y = H - 5*cm
for i, (val, label) in enumerate(metrics):
    col = i % cols
    row = i // cols
    bx = start_x + col * (box_w + 0.4*cm)
    by = start_y - row * (box_h + 0.4*cm)
    c.setFillColor(DARK if row == 0 else BLUE)
    c.roundRect(bx, by - box_h, box_w, box_h, 0.4*cm, fill=1, stroke=0)
    c.setFont("Arial-Bold", 24)
    c.setFillColor(ACCENT)
    c.drawCentredString(bx + box_w/2, by - box_h/2 + 0.3*cm, val)
    c.setFont("Arial", 10)
    c.setFillColor(colors.HexColor("#aaaaaa"))
    c.drawCentredString(bx + box_w/2, by - box_h/2 - 0.5*cm, label)

c.setFont("Arial-Bold", 12)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 12.2*cm, "Öğrendiklerimiz")
bullet_list([
    "<b>Test katmanları:</b> Unit hız sağlar, integration gerçekliği doğrular, E2E kullanıcı gözüyle bakar.",
    "<b>Container teknolojileri:</b> Docker Compose ile tekrar üretilebilir çok servisli ortam.",
    "<b>Gözlemlenebilirlik:</b> Prometheus + Grafana + OTel üçlüsü birlikte nasıl çalışır.",
], 1.2*cm, H - 12.9*cm, 30*cm, size=11)

c.setFont("Arial-Bold", 12)
c.setFillColor(DARK)
c.drawString(1.2*cm, H - 15.5*cm, "Zorluklar")
bullet_list([
    "Docker kurulumunda WSL 2 gerekliliği — kurulum ek zaman aldı.",
    "Testcontainers Windows ortamında Docker Desktop yapılandırması gerektirdi.",
    "Kubernetes manifest bağımlılıkları başlangıçta karmaşık geldi.",
], 1.2*cm, H - 16.2*cm, 30*cm, size=11)

c.showPage()

# ═══════════════════════════════════════════════════════════════════════════
# SLAYT 9 — TEŞEKKÜRLER / Q&A
# ═══════════════════════════════════════════════════════════════════════════
bg(DARK)
c.setFillColor(BLUE)
c.circle(W/2, H/2, 7*cm, fill=1, stroke=0)
c.setFillColor(ACCENT)
c.circle(W/2, H/2, 3*cm, fill=1, stroke=0)
c.setFillColor(WHITE)
c.setFont("Arial-Bold", 42)
c.drawCentredString(W/2, H/2 + 0.8*cm, "Teşekkürler")
c.setFont("Arial", 16)
c.setFillColor(colors.HexColor("#aaaaaa"))
c.drawCentredString(W/2, H/2 - 0.8*cm, "Sorularınız?")
c.setFont("Arial", 10)
c.setFillColor(colors.HexColor("#888888"))
c.drawCentredString(W/2, H - 1.5*cm, "Yasir ARSLAN  |  Büşra Ecem ÖZBEK  |  MTH2526-B25")
footer(9, TOTAL)
c.showPage()

c.save()

from pypdf import PdfReader
r = PdfReader(OUTPUT)
print(f"Slaytlar olusturuldu: {OUTPUT} — {len(r.pages)} slayt")
