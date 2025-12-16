# 🧠 Nasreddin Hoca AI - İki Modlu Gelişmiş Sohbet Asistanı

Bu proje, Python (Flask) ve OpenAI GPT-4o-mini kullanılarak geliştirilmiş, kültürel ve dini öğeler içeren interaktif bir yapay zeka sohbet botudur. Kullanıcılar, efsanevi halk bilgesi **Nasreddin Hoca** ile sohbet edebilir veya **Kur'an Modu**'na geçerek dini sorularına yanıt bulabilirler.

**Geliştirici:** Kaan

## 🌟 Özellikler

* **Çift Modlu Yapı:**
  * **Mod 1 (Normal Hoca):** Nasreddin Hoca'nın mizahi, nükteci ve bilge kişiliğini taklit eder. Fıkra anlatır ve öğüt verir.
  * **Mod 2 (Kur'an Hoca):** Sorulan sorulara sadece Kur'an ayetleri ve sureler ışığında, kaynak göstererek yanıt verir.
* **Dinamik Mod Değiştirme:** Sohbet akışı sırasında `/mod 1` veya `/mod 2` komutlarıyla anlık geçiş yapılabilir.
* **Akıllı Hafıza:** Yapay zeka, önceki konuşmaları hatırlar ve bağlama uygun cevaplar üretir.
* **Hibrit Veri Sistemi:** Sık sorulan sureler (Fatiha, İhlas vb.) için yerel veritabanını kullanır, karmaşık sorular için OpenAI API'ye başvurur.

## 🛠️ Kurulum ve Hazırlık

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler

* Python 3.8+
* OpenAI API Anahtarı

### 1. Projeyi İndirin

git clone [https://github.com/totem139/Nasreddin_Hoca_AI](https://github.com/totem139/Nasreddin_Hoca_AI)
cd nasreddin-hoca-ai


2. Gerekli Kütüphaneleri Yükleyin
Terminal veya komut satırında şu komutu çalıştırın:
pip install flask openai python-dotenv

3.. API Anahtarını Ayarlayın
Proje ana dizininde .env adında bir dosya oluşturun ve içine OpenAI API anahtarınızı ekleyin:
OPENAI_API_KEY=sk-sizin-api-anahtariniz-buraya
