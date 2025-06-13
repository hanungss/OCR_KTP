# 🪪 OCR KTP ke Excel 🇮🇩

Aplikasi Python untuk mengekstrak data dari gambar KTP Indonesia secara otomatis ke dalam file Excel.

Mendukung 3 metode OCR:
- 🔤 Tesseract OCR (offline, dasar)
- 🧠 EasyOCR (offline, AI, lebih akurat)
- ☁️ Google Cloud Vision API (online, sangat akurat)

---

## ✨ Fitur

- Input: Gambar KTP (.jpg/.jpeg/.png) di folder `image/`
- Output: File Excel (`output_ktp.xlsx`) berisi data terstruktur
- Ekstraksi otomatis:
  - NIK
  - Nama
  - Tempat & Tanggal Lahir (dipisah)
  - Jenis Kelamin, Gol. Darah
  - Alamat lengkap (dipisah: jalan, RT/RW, kelurahan, kecamatan)
  - Agama, Status, Pekerjaan, Kewarganegaraan, Masa Berlaku
- Pemrosesan batch (banyak file sekaligus)
- Modular, bisa pilih engine OCR

---

## 📂 Struktur Folder

```
OCR_KTP/
├── image/                      # Gambar KTP disimpan di sini
├── JSON/                       # Kunci akses Google Cloud Vision
│   └── ocr-access-key.json
├── ktp_ocr_to_excel.py         # Script utama
├── output_ktp.xlsx             # Hasil output (otomatis dibuat)
├── requirements.txt            # Daftar dependensi
└── README.md
```

---

## 🔧 Instalasi

### 1. Clone dan Masuk ke Folder
```bash
git clone https://github.com/hanungss/OCR_KTP.git
cd OCR_KTP
```

### 2. Aktifkan Virtual Environment (opsional)
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```

---

## 🚀 Menjalankan Script

### ✅ Mode 1: Tesseract (default)
```bash
python ktp_ocr_to_excel.py --mode tesseract
```

### ✅ Mode 2: EasyOCR (rekomendasi)
```bash
pip install easyocr
python ktp_ocr_to_excel.py --mode easyocr
```

### ✅ Mode 3: Google Cloud Vision (paling akurat)
1. Buat akun dan project di [Google Cloud Console](https://console.cloud.google.com/)
2. Aktifkan **Vision API** dan buat service account
3. Simpan file `ocr-access-key.json` di folder `JSON/`
4. Jalankan:
```bash
python ktp_ocr_to_excel.py --mode google
```

---

## 📦 Contoh Output (Excel)

| NIK              | Nama         | Tempat Lahir | Tanggal Lahir | Jenis Kelamin | ... |
|------------------|--------------|---------------|----------------|----------------|-----|
| 3171234567890123 | MIRA SETIAWAN| JAKARTA       | 18-02-1986     | PEREMPUAN      | ... |

---

## 🧠 Tips Akurasi

- Gunakan gambar beresolusi tinggi (>800px)
- Hindari gambar blur, miring, atau bayangan
- EasyOCR & Google Vision jauh lebih akurat dibanding Tesseract
- Gunakan Google Vision untuk kebutuhan produksi (meski butuh billing aktif)

---

## 📜 Lisensi

[MIT License](LICENSE)

---

## 🙋 Kontribusi

- Pull Request & saran sangat disambut!
- Kirim contoh KTP dummy atau masukan struktur parsing baru

---

## ☕ Creator

By [@hanungss](https://github.com/hanungss)
