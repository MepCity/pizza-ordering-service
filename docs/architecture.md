# Architecture Diagram

```mermaid
flowchart LR
    UI["Web UI / Postman / k6 / Playwright"] --> API["FastAPI Service"]
    API --> DB["PostgreSQL / SQLite"]
    API --> S3["LocalStack S3"]
    API --> METRICS["/metrics"]
    METRICS --> PROM["Prometheus"]
    PROM --> GRAF["Grafana"]
    DEV["GitHub Actions"] --> TESTS["Lint + Pytest + Newman"]
    TESTS --> IMAGE["Docker Image"]
    IMAGE --> K8S["Kubernetes / Minikube"]
    K8S --> API
```

## Components

- `FastAPI Service`: menu, order, coupon and status workflows
- `PostgreSQL / SQLite`: order and menu persistence
- `LocalStack S3`: order summary archive target
- `Prometheus`: metrics scraping from `/metrics`
- `Grafana`: latency, throughput and error rate dashboard
- `GitHub Actions`: lint, test, build and smoke pipeline
- `Kubernetes / Minikube`: deployment target for demo
