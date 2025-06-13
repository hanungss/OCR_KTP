import os
import re
import pandas as pd
from google.cloud import vision
from google.oauth2 import service_account

# Autentikasi Google Cloud dari folder JSON
creds = service_account.Credentials.from_service_account_file("JSON/ocr-access-key.json")
client = vision.ImageAnnotatorClient(credentials=creds)

# Fungsi parsing alamat
def parse_alamat(text):
    jalan = rtw = kel = kec = ""
    jalan_match = re.search(r'(Jl\.?|Jalan)[^RTK]*', text, re.IGNORECASE)
    rtw_match = re.search(r'RT\s*[\d]{1,3}/[\d]{1,3}', text)
    kel_match = re.search(r'Kel\.?\s*([A-Za-z\s]+)', text)
    kec_match = re.search(r'Kec\.?\s*([A-Za-z\s]+)', text)

    if jalan_match:
        jalan = jalan_match.group().strip()
    if rtw_match:
        rtw = rtw_match.group().replace("RT", "").strip()
    if kel_match:
        kel = kel_match.group(1).strip()
    if kec_match:
        kec = kec_match.group(1).strip()

    return jalan, rtw, kel, kec

# Fungsi parsing teks dari OCR
def parse_ktp_text(text):
    data = {
        "NIK": "",
        "Nama": "",
        "Tempat Lahir": "",
        "Tanggal Lahir": "",
        "Jenis Kelamin": "",
        "Jalan": "",
        "RT/RW": "",
        "Kelurahan": "",
        "Kecamatan": "",
        "Agama": "",
        "Pekerjaan": "",
        "Kewarganegaraan": ""
    }

    lines = text.split('\n')
    alamat_line = ""

    for line in lines:
        line = line.strip()
        if "NIK" in line and len(re.findall(r'\d{13,}', line)):
            data["NIK"] = ''.join(re.findall(r'\d{13,}', line))[0]
        elif "Nama" in line:
            data["Nama"] = line.split(":")[-1].strip()
        elif "Lahir" in line:
            parts = line.split(":")[-1].split(",")
            if len(parts) == 2:
                data["Tempat Lahir"] = parts[0].strip()
                data["Tanggal Lahir"] = parts[1].strip()
        elif "Jenis Kelamin" in line:
            data["Jenis Kelamin"] = line.split(":")[-1].strip()
        elif "Alamat" in line:
            alamat_line = line
        elif "Agama" in line:
            data["Agama"] = line.split(":")[-1].strip()
        elif "Pekerjaan" in line:
            data["Pekerjaan"] = line.split(":")[-1].strip()
        elif "Warga Negara" in line or "Kewarganegaraan" in line:
            data["Kewarganegaraan"] = line.split(":")[-1].strip()

    # Parsing alamat jika ditemukan
    if alamat_line:
        jalan, rtw, kel, kec = parse_alamat(alamat_line)
        data["Jalan"] = jalan
        data["RT/RW"] = rtw
        data["Kelurahan"] = kel
        data["Kecamatan"] = kec

    return data

# Fungsi OCR dari Google Vision
def ocr_gambar(image_path):
    with open(image_path, 'rb') as img_file:
        content = img_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else ""

# Proses semua gambar di folder
def process_all_images(folder="image"):
    hasil = []
    for fname in os.listdir(folder):
        if fname.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(folder, fname)
            print(f"🔍 Memproses {fname}")
            teks = ocr_gambar(path)
            data = parse_ktp_text(teks)
            data["File"] = fname
            hasil.append(data)
    return hasil

# Simpan ke Excel
def save_to_excel(data, output_file="output_ktp.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"✅ Disimpan ke {output_file}")

# Main
if __name__ == "__main__":
    semua_data = process_all_images("image")
    save_to_excel(semua_data)
