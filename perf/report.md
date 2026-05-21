# Performans Raporu

Bu rapor, yerel ortamda sandbox dışı çalıştırılan `Locust` yük testi sonucunda hazırlanmıştır. Şartname `k6` veya `Locust` kabul ettiği için ölçüm bu turda `Locust` ile alınmıştır.

## Test Kurulumu

- Host: `http://127.0.0.1:8001`
- Araç: `Locust 2.44.0`
- Sanal kullanıcı sayısı: `5`
- Artış oranı: `1 user/s`
- Süre: `15 saniye`
- Akışlar:
  - `GET /menu`
  - `POST /orders`
  - `PATCH /orders/{id}/status`

## Ölçüm Sonuçları

- Toplam istek: `66`
- Başarısız istek: `0`
- Ortalama gecikme: `7 ms`
- Medyan gecikme: `7 ms`
- p95 gecikme: `16 ms`
- Maksimum gecikme: `30 ms`
- Throughput: `4.63 req/s`

## Yorum

- p95 değeri `16 ms` olduğu için hedeflenen `500 ms` sınırının oldukça altında kalmıştır.
- Hata oranı `%0` olarak gözlemlenmiştir.
- Test süresi kısa ve kullanıcı sayısı düşüktür; bu yüzden sonuçlar başlangıç seviyesi bir performans göstergesi olarak değerlendirilmelidir.

## Örnek Çalıştırma

```bash
.venv/bin/uvicorn src.main:app --host 127.0.0.1 --port 8001
.venv/bin/locust -f perf/locustfile.py --host http://127.0.0.1:8001 --headless -u 5 -r 1 -t 15s --only-summary
```

## Notlar

- `k6` senaryosu da repoda korunmuştur: [perf/load-test.js](/Users/yasir.arslan/Desktop/bulut/perf/load-test.js)
- Docker daemon kapalı olduğunda Compose tabanlı ölçüm alınamadığı için bu raporda Locust sonucu kullanılmıştır.
