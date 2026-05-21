# Pizza Ordering Service

FastAPI tabanli minimal pizza siparis servisi. Projenin amaci, basit bir domain uzerinden test, CI/CD, container, Kubernetes, monitoring ve performans altyapisini gostermektir.

## Ozellikler

- Menu listeleme
- Siparis olusturma
- Siparis listeleme
- Siparis detayi goruntuleme
- Siparis durumu guncelleme
- Kupon uygulama
- Siparis ozetini S3'e arsivleme

## Teknoloji Yigini

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

## API Uclari

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

Sanal ortam ve bagimliliklar:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Uygulamayi lokal calistirma:

```bash
uvicorn src.main:app --reload
```

Uygulama varsayilan olarak `sqlite:///./pizza.db` ile acilir.

## Docker Compose

Tum servisleri ayağa kaldirma:

```bash
docker compose up --build
```

Bu komut su servisleri baslatir:

- `app`
- `postgres`
- `localstack`

## Testler

Unit testler:

```bash
pytest tests/unit -q
```

Tum testler:

```bash
pytest -q
```

Coverage:

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=70
```

Not:

- `tests/integration` altindaki Testcontainers testleri Docker gerektirir.
- Docker yoksa integration testler `skip` olur.

## Ortam Degiskenleri

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

Newman ile kosma ornegi:

```bash
newman run postman/collection.json --env-var baseUrl=http://127.0.0.1:8000
```

## Kubernetes

Ilk manifestler:

- [k8s/configmap.yaml](/Users/yasir.arslan/Desktop/bulut/k8s/configmap.yaml)
- [k8s/deployment.yaml](/Users/yasir.arslan/Desktop/bulut/k8s/deployment.yaml)
- [k8s/service.yaml](/Users/yasir.arslan/Desktop/bulut/k8s/service.yaml)

Uygulama image'i push edildikten sonra deploy:

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Monitoring

Hazirlanan temel dosyalar:

- [monitoring/prometheus.yml](/Users/yasir.arslan/Desktop/bulut/monitoring/prometheus.yml)
- [monitoring/grafana-dashboard.json](/Users/yasir.arslan/Desktop/bulut/monitoring/grafana-dashboard.json)

## Performans Testi

k6 senaryosu:

- [perf/load-test.js](/Users/yasir.arslan/Desktop/bulut/perf/load-test.js)

Calistirma ornegi:

```bash
k6 run perf/load-test.js
```

## Durum

Tamamlananlar:

- Temel API
- Unit testler
- PostgreSQL integration test omurgasi
- LocalStack S3 arsivleme
- Dockerfile
- Docker Compose
- CI iskeleti

Siradaki adimlar:

- Newman adimi
- Kubernetes dogrulamasi
- Monitoring dogrulamasi
- E2E arayuz ve Playwright
- Final rapor ve slaytlar
