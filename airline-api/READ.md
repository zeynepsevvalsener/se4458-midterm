# Airline Ticketing API

## Kurulum

1. `.env` dosyanı `.env.example` üzerinden oluştur, içindeki değerleri doldur.
2. `docker build -t airline_api .`
3. `docker run -d -p 8000:8000 --env-file .env airline_api`

## Swagger & Docs

- API dokümantasyonu: `http://localhost:8000/docs`

## Endpoints

- **POST** `/api/v1/auth/login` → Token alma  
- **POST** `/api/v1/flights` → Uçuş ekle (auth)  
- **GET**  `/api/v1/flights` → Uçuş sorgula (paging)  
- **POST** `/api/v1/tickets` → Bilet al (auth)  
- **POST** `/api/v1/tickets/checkin` → Check-in yap (auth)  
- **GET**  `/api/v1/tickets/passengers` → Yolcu listesi (auth, paging)

## Varsayımlar

- Basit `admin` kullanıcısı: kullanıcı adı `admin`, şifre `1234`.
- Hata yönetimi ve validasyonlar minimum düzeyde, gerçek projede genişletilmeli.
