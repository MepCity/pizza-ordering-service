from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Arial ile Türkçe karakter desteği
pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", "C:/Windows/Fonts/ariali.ttf"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic")

OUTPUT = "docs/final-report.pdf"

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=2.2*cm, rightMargin=2.2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
)

def style(name, **kwargs):
    base = dict(fontName="Arial", fontSize=10, leading=13, spaceAfter=4)
    base.update(kwargs)
    return ParagraphStyle(name, **base)

title_s  = style("title",  fontSize=15, leading=18, spaceAfter=4, alignment=1, fontName="Arial-Bold")
sub_s    = style("sub",    fontSize=10, spaceAfter=3, alignment=1, textColor=colors.HexColor("#444444"))
author_s = style("author", fontSize=10, spaceAfter=2, alignment=1)
h1_s     = style("h1",     fontSize=12, leading=15, spaceBefore=10, spaceAfter=5, fontName="Arial-Bold", textColor=colors.HexColor("#1a1a2e"))
h2_s     = style("h2",     fontSize=10, leading=13, spaceBefore=7, spaceAfter=3, fontName="Arial-Bold", textColor=colors.HexColor("#333333"))
body_s   = style("body",   fontSize=9,  leading=13, spaceAfter=4)
bullet_s = style("bullet", fontSize=9,  leading=13, spaceAfter=2, leftIndent=12)
small_s  = style("small",  fontSize=8,  leading=11, spaceAfter=2, textColor=colors.HexColor("#555555"))

def h1(t): return Paragraph(t, h1_s)
def h2(t): return Paragraph(t, h2_s)
def p(t):  return Paragraph(t, body_s)
def b(t):  return Paragraph(f"• {t}", bullet_s)
def sp(n=6): return Spacer(1, n)
def hr(): return HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#cccccc"), spaceAfter=6)

def table(data, widths, header_color="#1a1a2e"):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor(header_color)),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Arial-Bold"),
        ("FONTNAME",   (0,1), (-1,-1), "Arial"),
        ("FONTSIZE",   (0,0), (-1,-1), 8),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f8f8f8"), colors.white]),
        ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t

story = []

# ── Kapak ──────────────────────────────────────────────────────────────────
story += [
    sp(16),
    Paragraph("Pizza Ordering Service", title_s),
    Paragraph("Dönem Projesi Final Raporu", style("t2", fontSize=12, alignment=1, spaceAfter=4, fontName="Arial-Bold")),
    sp(4), hr(), sp(2),
    Paragraph("Bulut Mimarilerinde Test Mühendisliği | MTH2526-B25", sub_s),
    Paragraph("Marmara Üniversitesi — Bilgisayar Mühendisliği Bölümü", sub_s),
    sp(6),
    Paragraph("Yasir ARSLAN — 170423528", author_s),
    Paragraph("Büşra Ecem ÖZBEK — 170423966", author_s),
    sp(3),
    Paragraph("Haziran 2026", author_s),
    sp(16), hr(),
]

# ── 1. Giriş ───────────────────────────────────────────────────────────────
story += [
    sp(8),
    h1("1. Giriş"),
    p("Bu çalışmada, Bulut Mimarilerinde Test Mühendisliği dersi kapsamında "
      "<b>Pizza Ordering Service</b> adlı bir REST API mikroservisi geliştirilmiş ve "
      "endüstri standardında bir test ve dağıtım altyapısı kurulmuştur. Konu olarak "
      "pizza sipariş servisi seçilmesinin temel nedeni, domain'in yalın ve anlaşılır "
      "olması, buna karşın sipariş oluşturma, fiyatlandırma, durum geçişleri ve kupon "
      "yönetimi gibi test edilebilir iş kuralları barındırmasıdır."),
    p("Projenin amacı karmaşık bir uygulama yazmak değil; basit bir uygulama üzerinden "
      "unit test, integration test, E2E test, CI/CD pipeline, container, Kubernetes, "
      "monitoring ve performans testi katmanlarının tamamını uygulamalı olarak göstermektir."),
]

# ── 2. Mimari ──────────────────────────────────────────────────────────────
story += [
    h1("2. Mimari"),
    p("Uygulama, Docker Compose ile yönetilen çok servisli bir mikroservis mimarisiyle "
      "tasarlanmıştır. 7 servis tek komutla ayağa kalkar: app, postgres, localstack, "
      "prometheus, grafana, otel-collector, jaeger."),
    h2("2.1 Bileşenler"),
    b("<b>FastAPI (Python 3.12):</b> 7 endpoint sunar — /health, /menu, /orders (CRUD), durum güncelleme, kupon uygulama."),
    b("<b>SQLAlchemy + PostgreSQL 16:</b> ORM tabanlı veri katmanı. Lokalde SQLite, Docker/prod'da PostgreSQL kullanılır."),
    b("<b>LocalStack S3:</b> Sipariş özeti her oluşturmada orders/{id}.json anahtarıyla S3'e arşivlenir."),
    b("<b>Prometheus + Grafana:</b> /metrics toplanır; Request Throughput, Error Rate, Latency P95 panelleri."),
    b("<b>OpenTelemetry + Jaeger:</b> FastAPI, SQLAlchemy ve AWS çağrıları otomatik trace edilir."),
    b("<b>KEDA:</b> Prometheus metriğine göre 1–5 replica arasında otomatik ölçekleme."),
    b("<b>ArgoCD + Helm:</b> GitOps ile main branch'ten otomatik K8s deploy; Helm chart ile merkezi yönetim."),
    sp(3),
    h2("2.2 API Endpoint Tablosu"),
    table([
        ["Method", "Endpoint", "Açıklama"],
        ["GET", "/health", "Sağlık kontrolü (CI smoke + K8s probe)"],
        ["GET", "/menu", "Aktif menü öğelerini listele"],
        ["POST", "/orders", "Yeni sipariş oluştur (201)"],
        ["GET", "/orders", "Tüm siparişleri listele"],
        ["GET", "/orders/{id}", "Tek sipariş detayı (404 yoksa)"],
        ["PATCH", "/orders/{id}/status", "Durum güncelle (pending→preparing→ready→delivered)"],
        ["POST", "/orders/{id}/apply-coupon", "Kupon uygula (PIZZA10 / CHEESE20)"],
    ], [2.5*cm, 6.5*cm, 7.5*cm]),
]

# ── 3. Test Stratejisi ─────────────────────────────────────────────────────
story += [
    h1("3. Test Stratejisi"),
    p("Test piramidi yaklaşımı benimsenmiştir. Toplamda <b>18 test</b>, "
      "<b>%86 code coverage</b> (şart: %70)."),
    h2("3.1 Unit Testler — 11 adet (tests/unit/)"),
    p("SQLite in-memory DB kullanılır, 0.30 sn'de tamamlanır."),
    b("test_health.py: /health → 200 + {\"status\":\"ok\"}"),
    b("test_orders_api.py (8 test): Sipariş oluşturma, geçersiz extra (pineapple → 422), "
      "çift kupon → 400, geçersiz kupon kodu → 400, geçersiz durum geçişi (pending→delivered → 400), "
      "sıralı durum ilerlemesi, S3 arşiv tetiklenme."),
    b("test_order_archive.py: Factory Boy sahte sipariş → S3 JSON formatı doğrulaması."),
    b("test_web_ui.py: Ana sayfa HTML içeriği kontrolü."),
    h2("3.2 Integration Testler — 3 adet (tests/integration/)"),
    p("Testcontainers ile gerçek PostgreSQL 16 ve LocalStack container'ları başlatılır."),
    b("Sipariş gerçek DB'ye yazılıyor mu? Fiyat hesabı doğru mu?"),
    b("PIZZA10 kuponu sonrası DB'deki total_price güncelleniyor mu?"),
    b("Sipariş sonrası S3'te orders/{id}.json oluşuyor mu?"),
    h2("3.3 E2E Testler — 4 adet (tests/e2e/)"),
    p("Playwright Chromium ile gerçek tarayıcı, ayrı thread'de uvicorn sunucusu."),
    b("Sipariş oluşturma formu → yanıt doğrulama."),
    b("Sipariş listeleme ve detay görüntüleme."),
    b("Geçersiz extra → hata mesajı sayfada görünüyor mu?"),
    h2("3.4 Test Verisi Üretimi"),
    p("Factory Boy + Faker ile MenuItemFactory, OrderItemFactory, OrderFactory "
      "sınıfları yazılmıştır. Her çağrıda gerçekçi, rastgele ama geçerli veri üretilir."),
]

# ── 4. Pipeline ve Deploy ──────────────────────────────────────────────────
story += [
    h1("4. Pipeline ve Deploy"),
    h2("4.1 GitHub Actions CI/CD"),
    table([
        ["#", "Adım"],
        ["1-4", "Checkout → Python 3.11 → Node.js → kubectl → kind cluster"],
        ["5-6", "pip install -e .[dev] + newman + Playwright Chromium"],
        ["7", "Lint: ruff check ."],
        ["8", "pytest --cov=src --cov-fail-under=70"],
        ["9-10", "docker build + kind'a image yükle"],
        ["11-12", "kubectl apply (configmap, secret, service, deployment) + rollout status"],
        ["13", "Smoke test: port-forward + curl /health + Newman"],
    ], [2*cm, 14.5*cm]),
    sp(4),
    h2("4.2 Kubernetes Manifestleri"),
    b("<b>deployment.yaml:</b> 1 replica, /health probe, CPU 500m / RAM 256Mi limit."),
    b("<b>service.yaml:</b> ClusterIP, port 80 → container 8000."),
    b("<b>configmap.yaml:</b> Hassas olmayan env değişkenleri (DATABASE_URL vb.)."),
    b("<b>secret.yaml:</b> AWS anahtarları (hassas değişkenler)."),
    h2("4.3 Helm Chart ve ArgoCD"),
    b("charts/pizza-ordering-service/ — values.yaml ile image, replica, port merkezi yönetim."),
    b("ArgoCD: main branch'e merge → otomatik cluster deploy. prune + selfHeal aktif."),
]

# ── 5. Performans ve Gözlemlenebilirlik ────────────────────────────────────
story += [
    h1("5. Performans ve Gözlemlenebilirlik"),
    h2("5.1 Performans Testi"),
    p("k6 (perf/load-test.js) ve Locust (perf/locustfile.py) ile /menu, POST /orders "
      "ve GET /orders endpoint'lerine eş zamanlı yük uygulanmıştır. "
      "p95 latency ölçümü sonuçları perf/report.md dosyasında raporlanmıştır."),
    h2("5.2 Grafana Dashboard (3 Panel)"),
    b("<b>Request Throughput (req/s):</b> Trafik yoğunluğunu gösterir."),
    b("<b>Error Rate:</b> HTTP 5xx hata oranı."),
    b("<b>Latency P95:</b> İsteklerin %95'inin yanıt süresi."),
    h2("5.3 OpenTelemetry Distributed Tracing"),
    p("FastAPI, SQLAlchemy ve Botocore otomatik enstrümantasyonla izlenmektedir. "
      "Trace'ler Jaeger UI'da (localhost:16686) görüntülenebilir. "
      "Bir isteğin API'den DB'ye, oradan S3'e kadar tüm süreci tek ekranda takip edilebilir."),
]

# ── 6. Sonuç ──────────────────────────────────────────────────────────────
story += [
    h1("6. Sonuç ve Öğrendiklerimiz"),
    h2("6.1 Sayısal Özet"),
    table([
        ["Metrik", "Değer"],
        ["Toplam test", "18 (11 unit + 3 integration + 4 E2E)"],
        ["Code coverage", "%86 — şart %70, hedef aşıldı"],
        ["API endpoint", "7"],
        ["Docker servis", "7"],
        ["CI/CD adım", "13"],
        ["Bonus katman", "4 × +5 = +20 puan (Helm, KEDA, ArgoCD, OpenTelemetry)"],
    ], [8*cm, 8.5*cm]),
    sp(4),
    h2("6.2 Öğrendiklerimiz"),
    b("<b>Test katmanları:</b> Her katmanın farklı amacı olduğu pratik olarak gözlemlendi — "
      "unit hız, integration gerçeklik, E2E kullanıcı senaryosu."),
    b("<b>Container teknolojileri:</b> Docker Compose ile tekrar üretilebilir çok servisli "
      "ortam yönetimi deneyimi kazanıldı."),
    b("<b>Gözlemlenebilirlik:</b> Prometheus + Grafana + OpenTelemetry üçlüsünün birlikte "
      "nasıl çalıştığı kavrandı."),
    h2("6.3 Zorluklar"),
    b("Docker kurulumunda WSL 2 gerekliliği beklenmedik bir engel oluşturdu."),
    b("Testcontainers'ın Windows ortamında Docker Desktop yapılandırması gerekti."),
    b("Kubernetes manifest yazımı ve servisler arası bağımlılıklar başlangıçta karmaşık geldi."),
]

# ── 7. İş Paylaşımı ────────────────────────────────────────────────────────
story += [
    PageBreak(),
    h1("7. İş Paylaşımı"),
    table([
        ["Dosya / Modül", "Sorumlu", "Yardımcı"],
        ["src/main.py, src/api/routes.py", "Yasir ARSLAN", "B. Ecem ÖZBEK"],
        ["src/services/orders.py, pricing.py", "Yasir ARSLAN", "B. Ecem ÖZBEK"],
        ["src/integrations/order_archive.py, tracing.py", "Yasir ARSLAN", "—"],
        ["src/models/, src/schemas/, src/db/", "B. Ecem ÖZBEK", "Yasir ARSLAN"],
        ["tests/unit/ (tüm unit testler)", "Yasir ARSLAN", "B. Ecem ÖZBEK"],
        ["tests/unit/test_web_ui.py, tests/integration/", "B. Ecem ÖZBEK", "Yasir ARSLAN"],
        ["tests/conftest.py, factories.py", "B. Ecem ÖZBEK", "Yasir ARSLAN"],
        ["tests/e2e/test_ui_flow.py", "Yasir ARSLAN", "B. Ecem ÖZBEK"],
        ["Dockerfile, docker-compose.yml", "Yasir ARSLAN", "B. Ecem ÖZBEK"],
        ["k8s/deployment.yaml, service.yaml, scaledobject.yaml, argocd-application.yaml", "Yasir ARSLAN", "—"],
        ["k8s/configmap.yaml, secret.yaml", "B. Ecem ÖZBEK", "—"],
        [".github/workflows/ci.yml", "Yasir ARSLAN", "B. Ecem ÖZBEK"],
        ["monitoring/prometheus.yml, grafana-dashboard.json", "B. Ecem ÖZBEK", "Yasir ARSLAN"],
        ["monitoring/otel-collector-config.yaml", "Yasir ARSLAN", "—"],
        ["charts/pizza-ordering-service/ (Helm)", "Yasir ARSLAN", "B. Ecem ÖZBEK"],
        ["perf/load-test.js, perf/locustfile.py", "B. Ecem ÖZBEK", "—"],
        ["postman/collection.json", "Yasir ARSLAN", "—"],
        ["docs/architecture.md, architecture.png", "B. Ecem ÖZBEK", "Yasir ARSLAN"],
        ["pyproject.toml, README.md", "Yasir ARSLAN", "B. Ecem ÖZBEK"],
    ], [8.5*cm, 4.5*cm, 3.5*cm]),
    sp(6),
    h2("Sunum Sorumluluğu"),
    b("0–7 dk: Problem + Mimari + Test Stratejisi — Yasir ARSLAN"),
    b("7–14 dk: Canlı Demo (docker compose, API, Grafana, testler) — Büşra Ecem ÖZBEK"),
    b("14–17 dk: Sayılar + Öğrendiklerimiz — Yasir ARSLAN"),
    b("17–20 dk: Q&A — İkisi birlikte"),
]

# ── 8. Kaynaklar ───────────────────────────────────────────────────────────
story += [
    h1("8. Kaynaklar"),
    Paragraph("[1] FastAPI Resmi Dokümantasyonu — https://fastapi.tiangolo.com", small_s),
    Paragraph("[2] SQLAlchemy Dokümantasyonu — https://docs.sqlalchemy.org", small_s),
    Paragraph("[3] Docker Resmi Dokümantasyonu — https://docs.docker.com", small_s),
    Paragraph("[4] Testcontainers Python — https://testcontainers-python.readthedocs.io", small_s),
    Paragraph("[5] Playwright Python — https://playwright.dev/python", small_s),
    Paragraph("[6] Prometheus + Grafana Dokümantasyonu — https://prometheus.io/docs", small_s),
    Paragraph("[7] OpenTelemetry Python — https://opentelemetry.io/docs/instrumentation/python", small_s),
    Paragraph("[8] KEDA Dokümantasyonu — https://keda.sh/docs", small_s),
    Paragraph("[9] ArgoCD Dokümantasyonu — https://argo-cd.readthedocs.io", small_s),
    Paragraph("[10] Kubernetes Resmi Dokümantasyonu — https://kubernetes.io/docs", small_s),
    Paragraph("[11] k6 Yük Testi — https://k6.io/docs | Locust — https://docs.locust.io", small_s),
    Paragraph("[12] Docker Eğitim Videoları — YouTube", small_s),
]

doc.build(story)

# Sayfa sayısını kontrol et
from pypdf import PdfReader
r = PdfReader(OUTPUT)
print(f"PDF olusturuldu: {OUTPUT} — {len(r.pages)} sayfa")
