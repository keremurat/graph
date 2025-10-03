# 📊 Görsel Özellikler - JAMA Open PowerPoint Generator

Bu döküman, JAMA Network Open formatındaki PowerPoint sunumlarına eklenen görsel özellikleri açıklamaktadır.

## ✨ Özellikler

### 1. **Otomatik İkon Ekleme**

Her içerik kutusu için otomatik olarak uygun ikonlar oluşturulur:

- 👥 **POPULATION**: İnsan siluetleri (üç kişi gösterimi)
- 💊 **INTERVENTION**: Medikal haç (tedavi simgesi)
- 📊 **FINDINGS**: Bar grafik (veri görselleştirme)
- 🏥 **SETTINGS/LOCATIONS**: Hastane binası (lokasyon)
- 🎯 **PRIMARY OUTCOME**: Hedef/nişan tahtası (sonuç odaklılık)

İkonlar PowerPoint şekilleri kullanılarak vektörel olarak oluşturulur, bu yüzden kalite kaybı olmaz.

### 2. **İstatistiksel Grafik Üretimi**

FINDINGS bölümünde bulunan istatistiksel veriler otomatik olarak algılanır ve grafiğe dönüştürülür:

#### Desteklenen Veri Formatları:

```
Enhanced support: ~1.0
Foundational support: ~1.0
Mean difference: -0.1 (95% CI, -1.1 to 1.0)
P = .92
```

#### Grafik Türleri:

1. **Bar Chart (Karşılaştırma Grafiği)**
   - Gruplar arası karşılaştırma
   - Hata çubukları (error bars) ile güven aralıkları
   - P-değeri gösterimi

2. **Forest Plot** (Gelecek özellik)
   - Effect size gösterimi
   - Güven aralıkları

### 3. **Renk Şeması**

JAMA Network Open'ın resmi renk paleti:

- **Header**: `#E91383` (Magenta/Pink)
- **Aksan Rengi**: `#990066` (Koyu Magenta)
- **Kutular**: `#F0F0F0` (Açık Gri)
- **Metin**: `#323232` (Koyu Gri)

## 🔧 Kullanım

### Basit Kullanım

```bash
python main.py <JAMA_URL>
```

Varsayılan olarak JAMA Open formatında çıktı üretir ve otomatik olarak:
- İkonlar ekler
- Varsa istatistiksel grafikler oluşturur

### Format Seçimi

```bash
# JAMA Open formatı (görsellerle)
python main.py <URL> --format jama-open

# VA formatı (geleneksel)
python main.py <URL> --format va
```

### Verbose Mod

```bash
python main.py <URL> -v
```

Grafik üretimi sırasında hata/uyarıları görmek için verbose modu kullanın.

## 📦 Gereksinimler

Görsel özellikler için ek kütüphaneler:

```bash
pip install matplotlib pillow
```

Bu kütüphaneler olmadan:
- İkonlar yine de oluşturulur (PowerPoint shapes ile)
- Grafikler oluşturulmaz (sadece metin gösterilir)

## 🎨 Gelecek Özellikler

### Planlanan Geliştirmeler:

1. **AI Görsel Üretimi**
   ```bash
   python main.py <URL> --use-ai --api-key sk-ant-...
   ```
   - OpenAI DALL-E veya Anthropic Claude ile özel görseller
   - Çalışma konusuna özel illüstrasyonlar

2. **Gelişmiş Grafikler**
   - Forest plots
   - Kaplan-Meier eğrileri
   - ROC eğrileri
   - Funnel plots (meta-analizler için)

3. **Özelleştirilebilir Temalar**
   ```bash
   python main.py <URL> --theme custom --colors config.json
   ```

4. **Animasyonlar**
   - Grafiklerde fade-in efektleri
   - Sıralı görünüm

## 📝 Örnekler

### Örnek 1: Test Dosyası ile

```bash
python test_jama_open_format.py
```

Bu komut örnek verilerle bir sunum oluşturur ve tüm görsel özellikleri gösterir.

### Örnek 2: Gerçek Makale

```bash
python main.py "https://jamanetwork.com/journals/jamanetworkopen/fullarticle/XXXXX" -v
```

Gerçek bir JAMA makalesinden veri çekerek görsellerle zenginleştirilmiş sunum oluşturur.

## 🐛 Sorun Giderme

### Grafikler Oluşturulmuyor

1. Matplotlib ve Pillow kurulu olduğundan emin olun:
   ```bash
   pip install matplotlib pillow
   ```

2. Verbose mod ile detayları görün:
   ```bash
   python main.py <URL> -v
   ```

3. Veri formatını kontrol edin - desteklenen formatları yukarıda bulabilirsiniz

### İkonlar Görünmüyor

İkonlar PowerPoint'in yerleşik şekil kütüphanesi ile oluşturulur, ek kurulum gerektirmez.
Eğer görünmüyorlarsa, PowerPoint dosyasını farklı bir uygulamada açmayı deneyin.

## 🤝 Katkıda Bulunma

Yeni ikon tasarımları veya grafik türleri eklemek için:

1. `src/ppt_generator_jama_open.py` - İkonlar için
2. `src/chart_generator.py` - Grafikler için

Her iki dosya da iyi dökümente edilmiştir ve genişletilebilir yapıdadır.

## 📄 Lisans

Bu özellikler ana projenin lisansı altındadır.
