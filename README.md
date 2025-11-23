# 🕵️‍♂️ R10 Web X-RAY Bot v2.1

Bu araç, web siteleri üzerinde derinlemesine teknik analiz, güvenlik taraması ve altyapı tespiti yapan, Telegram tabanlı profesyonel bir OSINT aracıdır.

## 🌟 Özellikler

- **Tech Stack Detection:** CMS, Server, IP.
- **WordPress Scan:** Aktif tema ve eklenti tespiti.
- **Network Intel:** Whois verileri (Registrar, Dates).
- **Security Audit:** SSL Validity, Security Headers (HSTS, CF).
- **SEO Check:** Meta Tags & Response Time.

## ⚙️ Kurulum

1. Gerekli kütüphaneleri yükleyin (veya baslat.bat kullanın):
   ```bash
   pip install -r requirements.txt
.env dosyasını düzenleyin ve Telegram Tokeninizi girin:


BOT_TOKEN=12345:ABC...
Botu başlatın:

# Windows için
baslat.bat

# Terminal için
python main.py
📝 Kullanım
Botunuza /start yazın ve analiz etmek istediğiniz siteyi (örn: r10.net) gönderin.
