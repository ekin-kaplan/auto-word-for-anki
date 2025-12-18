# Lisan-ı Avni (LA) - Kelime Hazinesi Muhafızı

> **"Bir lisan, bir insan... Yedi lisan, bir cihandır."**  
> *Bu proje, Fatih Sultan Mehmet Han'ın yedi lisan bilme dehasından ilham alarak, Türk gençlerinin dünya dillerine hakimiyetini artırmak için milli bir duruşla hazırlanmıştır.*

---

![UI Preview](https://via.placeholder.com/800x400?text=Lisan-i+Avni+Arayuz)

## 🇹🇷 Neden Bu Proje?

Yabancı kaynaklara ve kapalı kutu sistemlere bağımlılık, uzun vadede **dijital esarettir**.

Biz, bilgiyi tüketmek yerine onu kendi algoritmalarımızla, kendi öğrenme metodolojimizle (Analoji Köprüsü) işleyerek millileştiriyoruz. **Lisan-ı Avni**, sadece bir kelime ezberleme aracı değil; yapay zekayı kendi kültürel ve eğitsel kodlarımızla yönetme iradesidir.

- **Analoji Köprüsü**: Kelimeleri kuru kuru ezberletmez; Türkçe benzetmelerle zihne nakşeder.
- **Milli Arayüz**: Saray Mavisi ve Altın renkleriyle asaletimizi yansıtır.
- **Hafıza Muhafızı**: Öğrenilen her kelimeyi Anki ile sonsuzluğa emânet eder.

## 🚀 Teknik Kurulum

Bu sistemi çalıştırmak bir fetih hazırlığı kadar titizlik gerektirir.

### 1. Hazırlık ve Cephane
Öncelikle Python (3.12+) ve Anki'nin bilgisayarınızda kurulu olduğundan emin olun.

```bash
# Projeyi klonlayın
git clone https://github.com/your-repo/lisan-i-avni.git
cd auto-word-for-anki

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt
```

### 2. AnkiConnect (Köprü Kurulumu)
Anki'nin dış dünya ile konuşması için kapıları açın:
1. Anki'yi açın.
2. `Araçlar` -> `Eklentiler` -> `Eklenti İndir` yolunu izleyin.
3. Şu kodu girin: **2055492159** (AnkiConnect).
4. Anki'yi **yeniden başlatın**.

### 3. Gemini API (Zeka Kaynağı)
1. `.env.example` dosyasının adını `.env` olarak değiştirin.
2. [Google AI Studio](https://aistudio.google.com/)'dan aldığınız API anahtarını buraya ekleyin:
   ```env
   GEMINI_API_KEY=AIzaSy...
   ```

### 4. Seferi Başlat
Komutan sizsiniz. Uygulamayı çalıştırın:
```bash
python main.py
```

## 🎯 Kullanım Kılavuzu

1. **Kelimeyi Keşfet**: Arayüze bir İngilizce kelime girin. Yapay zeka, o kelimenin Türkçe ruhunu ve analojisini bulup getirecektir.
2. **Analiz**: Gelen analojiyi okuyun. Eğer zihninize yattıysa...
3. **Hafızaya Emânet Et**: Butona basarak kelimeyi Anki'deki "Business English" destesine sonsuza dek kaydedin.

## 🤝 Katkı Çağrısı

Bu kaynak, Türk yazılımcıların katkısıyla büyüyecektir. Kodlarımızı inceleyin, geliştirin ve daha iyisini yapın.

**Gelin, dışa bağımlılığı azaltan bu eğitim devrimine omuz verin.**

---
*Kodlayan: Antigravity | Mimarı: Eko*
