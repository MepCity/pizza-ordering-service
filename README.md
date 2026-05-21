# Pizza Ordering Service

FastAPI tabanlı minimal pizza sipariş servisi. Projenin amacı, basit bir domain üzerinden test, CI/CD, container, Kubernetes, monitoring ve performans altyapısını göstermektir.

## Özellikler

- Menü listeleme
- Sipariş oluşturma
- Sipariş listeleme
- Sipariş detayı görüntüleme
- Sipariş durumu güncelleme
- Kupon uygulama
- Sipariş özetini S3'e arşivleme

## Teknoloji Yığını

- FastAPI
- SQLAlchemy
- PostgreSQL
- LocalStack S3
- Pytest
- Testcontainers
- Docker ve Docker Compose
- GitHub Actions
- Prometheus ve Grafana
- k6

## API Uçları

- `GET /health`
- `GET /menu`
- `POST /orders`
- `GET /orders`
- `GET /orders/{id}`
- `PATCH /orders/{id}/status`
- `POST /orders/{id}/apply-coupon`

## Lokal Kurulum

Gereksinimler:

- Python `3.11+` tavsiye edilir
- Docker
- Docker Compose

Sanal ortam ve bağımlılıklar:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Uygulamayı lokal çalıştırma:

```bash
uvicorn src.main:app --reload
```

Uygulama varsayılan olarak `sqlite:///./pizza.db` ile açılır.

## Docker Compose

Tüm servisleri ayağa kaldırma:

```bash
docker compose up --build
```

Bu komut şu servisleri başlatır:

- `app`
- `postgres`
- `localstack`
- `prometheus`
- `grafana`

Varsayılan arayüzler:

- API: `http://127.0.0.1:8000`
- Prometheus: `http://127.0.0.1:9090`
- Grafana: `http://127.0.0.1:3000`

Grafana giriş bilgileri:

- kullanıcı: `admin`
- şifre: `admin`

## Testler

Unit testler:

```bash
pytest tests/unit -q
```

Tüm testler:

```bash
pytest -q
```

Coverage:

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=70
```

Not:

- `tests/integration` altındaki Testcontainers testleri Docker gerektirir.
- Docker yoksa integration testler `skip` olur.

## Ortam Değişkenleri

- `DATABASE_URL`
- `S3_ARCHIVE_ENABLED`
- `S3_BUCKET_NAME`
- `AWS_REGION`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_ENDPOINT_URL`

## Postman ve Newman

Postman koleksiyonu:

- [postman/collection.json](/Users/yasir.arslan/Desktop/bulut/postman/collection.json)

Newman ile koşma örneği:

```bash
newman run postman/collection.json --env-var baseUrl=http://127.0.0.1:8000
```

## Kubernetes

İlk manifestler:

- [k8s/configmap.yaml](/Users/yasir.arslan/Desktop/bulut/k8s/configmap.yaml)
- [k8s/deployment.yaml](/Users/yasir.arslan/Desktop/bulut/k8s/deployment.yaml)
- [k8s/secret.yaml](/Users/yasir.arslan/Desktop/bulut/k8s/secret.yaml)
- [k8s/scaledobject.yaml](/Users/yasir.arslan/Desktop/bulut/k8s/scaledobject.yaml)
- [k8s/argocd-application.yaml](/Users/yasir.arslan/Desktop/bulut/k8s/argocd-application.yaml)
- [k8s/service.yaml](/Users/yasir.arslan/Desktop/bulut/k8s/service.yaml)

Uygulama image'i push edildikten sonra deploy:

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Monitoring

Hazırlanan temel dosyalar:

- [monitoring/prometheus.yml](/Users/yasir.arslan/Desktop/bulut/monitoring/prometheus.yml)
- [monitoring/grafana-dashboard.json](/Users/yasir.arslan/Desktop/bulut/monitoring/grafana-dashboard.json)
- [monitoring/grafana/provisioning/datasources/datasource.yml](/Users/yasir.arslan/Desktop/bulut/monitoring/grafana/provisioning/datasources/datasource.yml)
- [monitoring/grafana/provisioning/dashboards/dashboard.yml](/Users/yasir.arslan/Desktop/bulut/monitoring/grafana/provisioning/dashboards/dashboard.yml)
- [monitoring/otel-collector-config.yaml](/Users/yasir.arslan/Desktop/bulut/monitoring/otel-collector-config.yaml)

## Performans Testi

k6 senaryosu:

- [perf/load-test.js](/Users/yasir.arslan/Desktop/bulut/perf/load-test.js)

Çalıştırma örneği:

```bash
k6 run perf/load-test.js
```

## Durum

Tamamlananlar:

- Temel API
- Unit testler
- PostgreSQL integration test omurgası
- LocalStack S3 arşivleme
- Dockerfile
- Docker Compose
- CI iskeleti

Son durum:

- Newman adımı eklendi
- Kubernetes manifestleri hazırlandı
- Monitoring ve performans dosyaları hazırlandı
- E2E omurgası eklendi
- Final rapor, slayt ve mimari çıktı dosyaları üretildi

## Dokümanlar

- [docs/architecture.md](/Users/yasir.arslan/Desktop/bulut/docs/architecture.md)
- [docs/final-report.md](/Users/yasir.arslan/Desktop/bulut/docs/final-report.md)
- [docs/slides-outline.md](/Users/yasir.arslan/Desktop/bulut/docs/slides-outline.md)

## Bonus Çalışmalar

- Helm chart: [charts/pizza-ordering-service](/Users/yasir.arslan/Desktop/bulut/charts/pizza-ordering-service)
- KEDA autoscaling: [k8s/scaledobject.yaml](/Users/yasir.arslan/Desktop/bulut/k8s/scaledobject.yaml)
- ArgoCD application: [k8s/argocd-application.yaml](/Users/yasir.arslan/Desktop/bulut/k8s/argocd-application.yaml)
- OpenTelemetry collector: [monitoring/otel-collector-config.yaml](/Users/yasir.arslan/Desktop/bulut/monitoring/otel-collector-config.yaml)
