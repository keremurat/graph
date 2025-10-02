# 🎯 JAMA Makale → PowerPoint Dönüştürücü

JAMA Network'te yayınlanan klinik araştırma makalelerini otomatik olarak **Veterans Affairs (VA)** formatında profesyonel PowerPoint sunumlarına dönüştüren Python CLI uygulaması.

## ✨ Özellikler

### 🔄 3-Katmanlı Fallback Scraping Sistemi
- **Yöntem 1**: `requests` + `BeautifulSoup` (hızlı, basit)
- **Yöntem 2**: `Selenium` headless mode (JavaScript desteği)
- **Yöntem 3**: `Selenium` full browser (en güvenilir)
- Her yöntem başarısız olursa otomatik olarak sıradakini dener

### 🧠 Akıllı İçerik Çıkarma
- Makale başlığı, yazarlar, tarih, DOI otomatik çıkarma
- Abstract'tan yapılandırılmış veri çıkarma (Population, Intervention, Setting, Outcomes, Findings)
- Kelime limitleri ile otomatik özetleme
- Sayısal verileri regex ile akıllı yakalama (n=1234, 54.3%, p<0.05)

### 🎨 Otomatik İkon Seçimi
Makale içeriğine göre otomatik medikal alan tespiti:
- Cardiology (kardiyoloji)
- Neurology (nöroloji)
- Oncology (onkoloji)
- Respiratory (solunum)
- Diabetes (diyabet)
- Infectious (enfeksiyon)
- Mental Health (ruh sağlığı)
- Pediatric (pediatri)

### 📊 VA Format PowerPoint
- Profesyonel VA renk paleti (koyu mavi arka plan, beyaz kutular)
- 6 bilgi kutusu düzeni (Population, Intervention, Setting, Outcome, 2x Findings)
- Metin taşma koruması ve otomatik font boyutu ayarlama
- Yazar, tarih ve DOI bilgisi içeren footer

## 📦 Kurulum

### Gereksinimler
- Python 3.8+
- Chrome/Chromium tarayıcı (Selenium için)

### Adım 1: Projeyi klonlayın
```bash
cd jama-to-ppt
```

### Adım 2: Sanal ortam oluşturun (önerilen)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### Adım 3: Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

## 🚀 Kullanım

### Basit Kullanım
```bash
python main.py https://jamanetwork.com/journals/jama/fullarticle/12345
```

### Çıktı Yolu Belirtme
```bash
python main.py <URL> --output sunumum.pptx
```

### Verbose Mode (Detaylı Çıktı)
```bash
python main.py <URL> --verbose
```

### AI ile Gelişmiş Çıkarma (Opsiyonel)
```bash
python main.py <URL> --use-ai --api-key sk-ant-...
```

### Yardım
```bash
python main.py --help
```

## 📁 Proje Yapısı

```
jama-to-ppt/
├── src/
│   ├── __init__.py
│   ├── scraper.py          # 3-tier fallback scraping
│   ├── extractor.py        # İçerik çıkarma ve özetleme
│   ├── ppt_generator.py    # VA format PowerPoint oluşturma
│   └── utils.py            # İkon seçimi ve yardımcı fonksiyonlar
├── templates/
│   └── va_template.pptx    # (Opsiyonel) Hazır şablon
├── tests/
│   ├── test_scraper.py
│   ├── test_extractor.py
│   └── test_ppt.py
├── output/                  # Oluşturulan sunumlar
├── main.py                  # CLI giriş noktası
├── requirements.txt
└── README.md
```

## 🎨 VA Format Özellikleri

### Renk Paleti
- **Arka plan**: `#003366` (koyu mavi)
- **Başlık**: Beyaz, bold, 24pt (uzun başlıklar için 18pt)
- **Kutu arka planı**: Beyaz
- **Kutu çerçevesi**: VA mavi, 2pt kalınlık
- **Footer**: Açık gri, 9pt

### Düzen
```
┌─────────────────────────────────────┐
│     [MAKALE BAŞLIĞI - VURGULU]      │
├─────────────────────────────────────┤
│  ┌──────────┐      ┌──────────┐    │
│  │Population│      │Intervention│   │
│  └──────────┘      └──────────┘    │
│                                     │
│  ┌──────────┐      ┌──────────┐    │
│  │ Setting  │      │  Primary   │   │
│  │          │      │  Outcome   │   │
│  └──────────┘      └──────────┘    │
│                                     │
│  ┌──────────┐      ┌──────────┐    │
│  │Finding 1 │      │ Finding 2 │    │
│  └──────────┘      └──────────┘    │
├─────────────────────────────────────┤
│ [Yazar, Tarih, DOI - Alt bilgi]    │
└─────────────────────────────────────┘
```

### Kelime Limitleri
- **Population**: 15 kelime
- **Intervention**: 15 kelime
- **Setting**: 10 kelime
- **Primary Outcome**: 20 kelime
- **Findings**: 15'er kelime

## 🧪 Test Örnekleri

### Test Case 1: Kardiyoloji
```bash
python main.py "https://jamanetwork.com/journals/jama/fullarticle/[cardiology-article-id]" --verbose
```
- "cardiac", "heart" kelimeleri → `cardiology` ikonu seçilmeli
- Uzun başlık → Font boyutu 18pt'e düşmeli

### Test Case 2: Nöroloji
```bash
python main.py "https://jamanetwork.com/journals/jama/fullarticle/[neurology-article-id]"
```
- "Alzheimer", "cognitive" → `neurology` ikonu
- Abstract'tan sayısal veriler çıkarılmalı

### Test Case 3: Erişim Sorunu
- Yöntem 1 başarısız → Yöntem 2 denenmeli
- Tüm yöntemler başarısız → Net hata mesajı

## ⚙️ Teknik Detaylar

### Hata Yönetimi
- Try-except blokları ile güvenli çalışma
- Her aşamada kullanıcıya bilgilendirme
- Graceful degradation (program çökmez)
- Emoji ile görsel hata mesajları (✅, ❌, ⚠️)

### Progress İndikatörleri
```
🔄 Yöntem 1 deneniyor: requests...
✅ Başarılı! (Yöntem 2)
🔍 İçerik analiz ediliyor...
📝 PowerPoint oluşturuluyor...
✨ İşlem tamamlandı!
```

### Metin Taşma Koruması
1. `word_wrap=True` aktif
2. Taşma varsa font: 10pt → 9pt → 8pt
3. Hala taşarsa "..." ile kırp

## 🔮 Gelecek Özellikler (Sprint 3)

- [ ] AI destekli içerik çıkarma (Anthropic API)
- [ ] Şablon desteği (custom PPTX template)
- [ ] Batch processing (çoklu URL)
- [ ] Web UI (Streamlit/Gradio)
- [ ] Grafik/tablo çıkarma
- [ ] Çoklu dil desteği

## 📝 Lisans ve Kullanım

**Önemli:** Bu proje bir **araştırma ve eğitim aracı**dır. Telif hakları nedeniyle:
- Makalelerin tam metni kopyalanmaz
- Sadece özetleme ve görselleştirme yapılır (fair use)
- Ticari kullanım için izin gerekebilir

## 🐛 Bilinen Sorunlar ve Çözümler

### Problem: Selenium ChromeDriver hatası
**Çözüm:**
```bash
pip install --upgrade webdriver-manager
```

### Problem: JAMA sayfası yüklenmiyor
**Çözüm:**
- VPN kullanıyorsanız kapatın
- `--verbose` ile hangi yöntemin çalıştığını kontrol edin
- URL'yi tarayıcıda manuel olarak test edin

### Problem: Abstract bulunamıyor
**Çözüm:**
- Bazı makaleler "paywall" arkasında olabilir
- Premium erişim gerektirebilir
- Alternatif URL deneyin (PubMed, DOI.org)

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing`)
3. Commit yapın (`git commit -m 'feat: Add amazing feature'`)
4. Push edin (`git push origin feature/amazing`)
5. Pull Request açın

## 📧 İletişim

Sorularınız için issue açın veya e-posta gönderin.

---

**Made with ❤️ for medical research community**
