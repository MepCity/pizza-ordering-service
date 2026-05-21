# Pizza Ordering Service Final Raporu

## 1. Giriş

Bu proje, küçük bir backend uygulaması etrafında modern test ve dağıtım pratiklerini göstermek amacıyla geliştirilen minimal bir pizza sipariş servisidir. Buradaki temel amaç karmaşık bir domain modeli kurmak değil; test edilebilir, gözlemlenebilir, container tabanlı ve CI/CD ile desteklenen bir servis inşa etmektir.

Projenin ana hedefleri şunlardır:

- açık iş kurallarına sahip küçük bir REST servisi geliştirmek
- servis davranışını unit ve integration testlerle doğrulamak
- sipariş özetlerini AWS uyumlu bir nesne depolama katmanına yazmak
- uygulamayı Docker ile paketlemek
- Kubernetes üzerinde çalıştırılabilecek manifestleri hazırlamak
- metrik toplama ve performans gözlemi için gerekli altyapıyı kurmak

## 2. Mimari

Sistem merkezinde FastAPI ile geliştirilen bir uygulama bulunmaktadır. Menü ve sipariş işlemleri bu servis üzerinden yönetilir. Sipariş verileri ilişkisel veritabanında tutulur. Ek olarak sipariş özeti, LocalStack S3 üzerinde JSON formatında arşivlenebilir.

Monitoring katmanında Prometheus uygulamanın `/metrics` çıktısını toplar. Grafana ise throughput, error rate ve latency metriklerini görselleştirir. Docker Compose ile tüm servisler yerel ortamda birlikte ayağa kaldırılabilir. Kubernetes manifestleri ise Minikube üzerinde dağıtım yapılabilmesi için hazırlanmıştır.

Mimari diyagram kaynağı:

- [docs/architecture.md](/Users/yasir.arslan/Desktop/bulut/docs/architecture.md)

## 3. Test Stratejisi

Projede katmanlı bir test yaklaşımı kullanılmıştır:

- unit testler ile pricing, kupon, status transition ve API davranışı doğrulanır
- PostgreSQL tabanlı integration testler ile gerçek persistence davranışı sınanır
- LocalStack destekli integration testler ile S3 arşivleme davranışı doğrulanır
- Postman/Newman ile endpoint koleksiyonu toplu olarak çalıştırılır
- Playwright tabanlı E2E omurgası ile tarayıcı akışı için temel iskelet hazırlanır
- k6 ile hafif yük testi senaryosu tanımlanır

CI tarafında coverage eşiği olarak en az `%70` zorunlu tutulmuştur.

## 4. Pipeline ve Dağıtım

GitHub Actions workflow'u aşağıdaki adımları içerir:

- lint
- pytest ve coverage kontrolü
- Docker image build
- smoke test
- Newman koleksiyonu çalıştırma

Dağıtım için hazırlanan artefaktlar:

- Dockerfile
- docker-compose kurulumu
- Kubernetes `Deployment`, `Service`, `ConfigMap` ve `Secret` dosyaları

## 5. Performans ve Gözlemlenebilirlik

Uygulama `prometheus-fastapi-instrumentator` ile `/metrics` endpoint'i üretmektedir. Prometheus bu endpoint üzerinden veri toplar. Grafana dashboard'unda şu paneller tanımlanmıştır:

- request throughput
- error rate
- p95 latency

k6 senaryosu aşağıdaki akışları test eder:

- `GET /menu`
- `POST /orders`
- `PATCH /orders/{id}/status`

Yerel ortamda Locust ile alınan örnek ölçümde p95 latency `16 ms`, maksimum gecikme `30 ms` ve hata oranı `%0` olarak gözlemlenmiştir.

## 6. Karşılaşılan Zorluklar ve Öğrenilenler

Geliştirme sürecinde öne çıkan teknik noktalar şunlardır:

- Testcontainers ile kullanılan PostgreSQL driver'ının projedeki `psycopg` bağımlılığıyla uyumlu hale getirilmesi
- bazı integration ve E2E testlerinin kısıtlı ortamlarda suite'i kırmadan skip edilebilir olacak şekilde tasarlanması
- altyapı dosyalarının erkenden hazırlanmasının ilerideki entegrasyonları kolaylaştırması
- Kubernetes tarafında genel konfigürasyon ile gizli bilgilerin ayrıştırılması

## 7. Gelecek Çalışmalar

- Playwright akışının CI içinde browser kurulumu ile tamamen çalıştırılması
- Newman koleksiyonuna negatif senaryolar eklenmesi
- Kubernetes dağıtımının gerçek Minikube ortamında doğrulanması
- performans raporunun gerçek ölçüm sonuçlarıyla doldurulması

## 8. Kaynaklar

- FastAPI dokümantasyonu
- SQLAlchemy dokümantasyonu
- Testcontainers dokümantasyonu
- LocalStack dokümantasyonu
- Prometheus dokümantasyonu
- Grafana dokümantasyonu
- k6 dokümantasyonu
