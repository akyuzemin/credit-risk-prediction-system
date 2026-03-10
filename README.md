# Credit Risk Prediction System

Kredi başvurusu yapan kullanıcıların bilgilerine göre ön değerlendirme sonucu üreten full-stack bir uygulamadır. Sistem, başvuru bilgilerini analiz ederek kullanıcının genel kredi uygunluk durumunu, risk seviyesini, risk oranını ve başvuruyu güçlendirmek için kısa önerileri gösterir.

## Proje Özeti

Bu proje iki ana parçadan oluşur:

- **Backend:** FastAPI
- **Frontend:** React + Vite

Uygulama, kredi başvurusu için girilen bilgileri değerlendirir ve kullanıcıya şu çıktıları sunar:

- başvuru durumu
- risk seviyesi
- risk oranı
- değerlendirme özeti
- başvuruyu güçlendirmek için öneriler

## Özellikler

- Kullanıcı dostu kredi uygunluk ön değerlendirme ekranı
- Türkçe arayüz
- Risk seviyesi gösterimi
- Risk oranı gösterimi
- Başlıca etkileyen unsurların listelenmesi
- FastAPI tabanlı REST API
- React tabanlı modern frontend

## Kullanılan Teknolojiler

### Backend
- Python
- FastAPI
- Pandas
- Scikit-learn
- Joblib

### Frontend
- React
- Vite
- TypeScript
- Tailwind / shadcn UI

## Proje Yapısı

```text
credit-risk-prediction-system_fullstack
├── app
├── src
├── configs
├── models
├── reports
├── creditview-dashboard
└── requirements.txt

Backend Çalıştırma
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Backend test adresi:
http://127.0.0.1:8000/health

Frontend Çalıştırma
cd creditview-dashboard
npm install
npm run dev

Frontend Adresi:
http://localhost:8080

Uygulamanın Amacı

Bu uygulama, kullanıcıların kredi başvurusuna dair temel bilgileri girerek hızlı bir ön değerlendirme sonucu almasını sağlar. Amaç, teknik model ayrıntılarını göstermek yerine kullanıcıya anlaşılır ve sade bir karar ekranı sunmaktır.

Çıktılar

Kullanıcı sistem üzerinden aşağıdaki bilgileri görür:

Başvuru Durumu: Uygun / Ek İnceleme Gerekli / Uygun Değil

Risk Seviyesi: Düşük / Orta / Yüksek

Risk Oranı: Yüzdesel tahmini risk değeri

Değerlendirme Özeti

Başvuruyu Güçlendirmek İçin Öneri


Not

Bu uygulama yalnızca ön değerlendirme amacı taşır. Nihai kredi kararı gerçek banka prosedürleri ve resmi değerlendirme süreçleri doğrultusunda verilir.

