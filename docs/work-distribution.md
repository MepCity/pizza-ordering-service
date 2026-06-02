# İş Paylaşımı — Pizza Ordering Service

## Üyeler

- Yasir ARSLAN (170423528) — Backend & DevOps, repo sahibi
- Büşra Ecem ÖZBEK (170423966) — Modeller, DB, Monitoring & Test

## Modül Sorumluluğu

| Dosya / Modül | Sorumlu | Yardımcı |
|---|---|---|
| `src/main.py` | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `src/api/routes.py` | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `src/services/orders.py` | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `src/services/pricing.py` | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `src/integrations/order_archive.py` | Yasir ARSLAN | — |
| `src/integrations/tracing.py` | Yasir ARSLAN | — |
| `src/models/` | Büşra Ecem ÖZBEK | Yasir ARSLAN |
| `src/schemas/` | Büşra Ecem ÖZBEK | Yasir ARSLAN |
| `src/db/` | Büşra Ecem ÖZBEK | Yasir ARSLAN |
| `tests/conftest.py` | Büşra Ecem ÖZBEK | Yasir ARSLAN |
| `tests/factories.py` | Büşra Ecem ÖZBEK | Yasir ARSLAN |
| `tests/unit/test_orders_api.py` | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `tests/unit/test_health.py` | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `tests/unit/test_order_archive.py` | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `tests/unit/test_web_ui.py` | Büşra Ecem ÖZBEK | Yasir ARSLAN |
| `tests/integration/conftest.py` | Büşra Ecem ÖZBEK | Yasir ARSLAN |
| `tests/integration/test_orders_postgres.py` | Büşra Ecem ÖZBEK | Yasir ARSLAN |
| `tests/e2e/test_ui_flow.py` | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `Dockerfile` | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `docker-compose.yml` | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `k8s/deployment.yaml` | Yasir ARSLAN | — |
| `k8s/service.yaml` | Yasir ARSLAN | — |
| `k8s/scaledobject.yaml` | Yasir ARSLAN | — |
| `k8s/argocd-application.yaml` | Yasir ARSLAN | — |
| `k8s/configmap.yaml` | Büşra Ecem ÖZBEK | — |
| `k8s/secret.yaml` | Büşra Ecem ÖZBEK | — |
| `.github/workflows/ci.yml` | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `monitoring/prometheus.yml` | Büşra Ecem ÖZBEK | Yasir ARSLAN |
| `monitoring/grafana-dashboard.json` | Büşra Ecem ÖZBEK | Yasir ARSLAN |
| `monitoring/otel-collector-config.yaml` | Yasir ARSLAN | — |
| `charts/pizza-ordering-service/` (Helm) | Yasir ARSLAN | Büşra Ecem ÖZBEK |
| `perf/load-test.js` | Büşra Ecem ÖZBEK | — |
| `perf/locustfile.py` | Büşra Ecem ÖZBEK | — |
| `postman/collection.json` | Yasir ARSLAN | — |
| `docs/architecture.md`, `architecture.png` | Büşra Ecem ÖZBEK | Yasir ARSLAN |
| `pyproject.toml`, `README.md` | Yasir ARSLAN | Büşra Ecem ÖZBEK |

## Sunum Sorumluluğu (20 dk slot)

| Süre | İçerik | Sunan |
|---|---|---|
| 0–7 dk | Problem + Mimari + Test Stratejisi | Yasir ARSLAN |
| 7–14 dk | Canlı Demo (docker compose → API → Grafana → testler) | Büşra Ecem ÖZBEK |
| 14–17 dk | Sayılar + Öğrendiklerimiz | Yasir ARSLAN |
| 17–20 dk | Q&A | İkisi birlikte |
