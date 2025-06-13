import os
import re
import pytesseract
import pandas as pd
import cv2
from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Untuk Windows

def ocr_gambar(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)
    text = pytesseract.image_to_string(blur, lang='eng+ind')  # tambah bahasa jika perlu
    return text

def parse_teks(text):
    data = {
        "NIK": "", "Nama": "", "Tempat Lahir": "", "Tanggal Lahir": "",
        "Jenis Kelamin": "", "Gol Darah": "", "Jalan": "", "RT/RW": "",
        "Kelurahan": "", "Kecamatan": "", "Agama": "", "Status": "",
        "Pekerjaan": "", "Kewarganegaraan": "", "Berlaku Hingga": ""
    }

    text = text.replace("\n", " ")
    text = re.sub(r"\s{2,}", " ", text)

    nik = re.search(r"\d{16}", text)
    nama = re.search(r"Nama\s*:\s*([A-Z\s]+)", text)
    ttl = re.search(r"Tempat/Tgl Lahir\s*:\s*([A-Za-z]+),?\s*(\d{2}-\d{2}-\d{4})", text)
    jk = re.search(r"Jenis Kelamin\s*:\s*(\w+)", text)
    goldar = re.search(r"Gol\.?\s*Darah\s*:\s*(\w+)", text)
    alamat = re.search(r"Alamat\s*:\s*([^R]+)", text)
    rtrw = re.search(r"RT/RW\s*:\s*(\d+/\d+)", text)
    kel = re.search(r"Kel/Desa\s*:\s*([A-Z\s]+)", text)
    kec = re.search(r"Kecamatan\s*:\s*([A-Z\s]+)", text)
    agama = re.search(r"Agama\s*:\s*([A-Z]+)", text)
    status = re.search(r"Status Perkawinan\s*:\s*([A-Z]+)", text)
    pekerjaan = re.search(r"Pekerjaan\s*:\s*([A-Z\s]+)", text)
    kewarganegaraan = re.search(r"Kewarganegaraan\s*:\s*([A-Z]+)", text)
    berlaku = re.search(r"Berlaku Hingga\s*:\s*(\d{2}-\d{2}-\d{4})", text)

    if nik: data["NIK"] = nik.group()
    if nama: data["Nama"] = nama.group(1).strip()
    if ttl:
        data["Tempat Lahir"] = ttl.group(1).strip()
        data["Tanggal Lahir"] = ttl.group(2).strip()
    if jk: data["Jenis Kelamin"] = jk.group(1)
    if goldar: data["Gol Darah"] = goldar.group(1)
    if alamat: data["Jalan"] = alamat.group(1).strip()
    if rtrw: data["RT/RW"] = rtrw.group(1)
    if kel: data["Kelurahan"] = kel.group(1).strip()
    if kec: data["Kecamatan"] = kec.group(1).strip()
    if agama: data["Agama"] = agama.group(1)
    if status: data["Status"] = status.group(1)
    if pekerjaan: data["Pekerjaan"] = pekerjaan.group(1).strip()
    if kewarganegaraan: data["Kewarganegaraan"] = kewarganegaraan.group(1)
    if berlaku: data["Berlaku Hingga"] = berlaku.group(1)

    return data

def proses_folder(folder="image"):
    hasil = []
    for nama_file in os.listdir(folder):
        if nama_file.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(folder, nama_file)
            print(f"🔍 Memproses {nama_file}")
            text = ocr_gambar(path)
            data = parse_teks(text)
            data["File"] = nama_file
            hasil.append(data)
    return hasil

def simpan_excel(data, nama_file="output_ktp.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(nama_file, index=False)
    print(f"✅ Disimpan ke {nama_file}")

if __name__ == "__main__":
    hasil = proses_folder("image")
    simpan_excel(hasil)
