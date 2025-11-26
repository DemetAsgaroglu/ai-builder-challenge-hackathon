# 🧮 AI Calculator Agent

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B)](https://ai-builder-challenge-hackathon-ct8oekmwqowad4cd2znxjp.streamlit.app/)

**🌐 Canlı Demo**: [https://ai-builder-challenge-hackathon-ct8oekmwqowad4cd2znxjp.streamlit.app/](https://ai-builder-challenge-hackathon-ct8oekmwqowad4cd2znxjp.streamlit.app/)

**Google Gemini Gen AI SDK** ile güçlendirilmiş, doğal dil işleme yeteneğine sahip akıllı hesaplama asistanı.

## 🌟 Özellikler

Bu proje, standart bir hesap makinesinin ötesine geçerek karmaşık matematiksel ve finansal problemleri doğal dille çözebilir.

*   **🧮 Temel Matematik**: Dört işlem, trigonometri, logaritma.
*   **∫ Kalkülüs**: Türev, integral, limit hesaplamaları.
*   **📐 Lineer Cebir**: Matris işlemleri, determinant, özdeğerler.
*   **💰 Finans**: Kredi hesaplama, faiz, NPV, IRR.
*   **📊 İstatistik (YENİ)**: Veri seti analizi, ortalama, standart sapma.
*   **📈 Grafik Çizimi**: Fonksiyonların görselleştirilmesi (`sin(x)`, `x^2` vb.).
*   **💬 Sohbet Modu**: Matematik dışı konularda genel asistan desteği.

## 🚀 Kurulum

1.  **Repository'yi Klonlayın**
    ```bash
    git clone https://github.com/KULLANICI_ADINIZ/calculator-agent.git
    cd calculator-agent
    ```

2.  **Sanal Ortam Oluşturun (Önerilen)**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Bağımlılıkları Yükleyin**
    ```bash
    pip install -r requirements.txt
    ```

4.  **API Anahtarını Ayarlayın**
    `.env.example` dosyasının adını `.env` olarak değiştirin ve Google Gemini API anahtarınızı ekleyin.
    ```text
    GEMINI_API_KEY=sizin_api_anahtariniz
    ```

## 💻 Kullanım

Projeyi iki farklı şekilde kullanabilirsiniz:

### 1. Web Arayüzü (Streamlit) 🌟
Modern ve kullanıcı dostu web arayüzü için:
```bash
streamlit run src/streamlit_app.py
```

### 2. Terminal (CLI)
Klasik komut satırı arayüzü için:
```bash
python src/main.py
```

## 📂 Proje Yapısı

Projenin önemli dosya ve klasörleri aşağıda açıklanmıştır:

```text
calculator-agent/
├── src/
│   ├── main.py                 # 🏁 Ana uygulama ve Terminal arayüzü
│   ├── streamlit_app.py        # 🌟 Streamlit Web Arayüzü
│   ├── core/
│   │   ├── agent.py            # 🤖 Google Gemini AI entegrasyonu
│   │   ├── parser.py           # 🗣️ Doğal dil işleme ve komut ayrıştırma
│   │   └── validator.py        # 🛡️ Güvenlik ve girdi doğrulama
│   ├── modules/                # 🧮 Hesaplama modülleri
│   │   ├── basic_math.py       # Temel matematik işlemleri
│   │   ├── calculus.py         # Kalkülüs (Türev, İntegral)
│   │   ├── statistics.py       # İstatistik (Yeni Modül)
│   │   ├── graph_plotter.py    # Grafik çizimi
│   │   └── ...                 # Diğer modüller (Finans, Lineer Cebir vb.)
│   └── config/                 # ⚙️ Ayarlar ve Promptlar
├── tests/                      # 🧪 Birim testleri (Unit Tests)
├── .github/workflows/ci.yml    # 🔄 CI/CD Otomasyon dosyası
├── HACKATHON_SOLUTIONS.md      # 📝 Çözülen hataların detaylı raporu
├── verify_all.py               # ✅ Sistemin uçtan uca doğrulama testi
├── requirements.txt            # 📦 Proje bağımlılıkları
└── README.md                   # 📖 Proje dokümantasyonu
```

## 🌐 Canlıya Alma (Deployment)

Bu projeyi **Streamlit Community Cloud** üzerinde ücretsiz olarak yayınlayabilirsiniz:

1.  Kodlarınızı GitHub'a yükleyin.
2.  [share.streamlit.io](https://share.streamlit.io) adresine gidin.
3.  Repository'nizi seçin ve `src/streamlit_app.py` dosyasını ana dosya olarak belirtin.
4.  **Deploy** butonuna basın!

## 🛠️ Hackathon Çözümleri

Bu proje, **AI Builder Challenge Hackathon** kapsamında geliştirilmiştir. Projede başlangıçta bulunan **12 kritik hata** ve **100+ syntax hatası** giderilmiştir.

Detaylı hata raporu ve çözüm yöntemleri için lütfen **[HACKATHON_SOLUTIONS.md](HACKATHON_SOLUTIONS.md)** dosyasını inceleyin.

### Başarımlar
- ✅ **Level 1-2-3 Hataları**: Tümü giderildi.
- ✅ **Yeni Modül**: İstatistik modülü eklendi.
- ✅ **CI/CD**: GitHub Actions ile otomatik test süreci kuruldu.
- ✅ **UI**: Streamlit ile web arayüzü geliştirildi.

## 🧪 Testler

Sistemin doğruluğunu kontrol etmek için:

```bash
# Tüm birim testleri çalıştır
pytest

# Uçtan uca doğrulama testi
python verify_all.py
```

---
*Developed for AI Builder Challenge Hackathon 2025*
