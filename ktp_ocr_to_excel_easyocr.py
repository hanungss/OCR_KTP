import easyocr
import cv2
import os
import pandas as pd

reader = easyocr.Reader(['id'])  # bahasa Indonesia

def proses_ktp(image_path):
    result = reader.readtext(image_path, detail=0)
    full_text = " ".join(result)

    # Parsing manual (bisa kita tingkatkan)
    data = {
        "NIK": "",
        "Nama": "",
        "Tempat Lahir": "",
        "Tanggal Lahir": "",
        "Jenis Kelamin": "",
        "Gol Darah": "",
        "Alamat": "",
        "RT/RW": "",
        "Kelurahan": "",
        "Kecamatan": "",
        "Agama": "",
        "Status": "",
        "Pekerjaan": "",
        "Kewarganegaraan": "",
        "Berlaku Hingga": ""
    }

    # Parsing contoh (bisa disesuaikan)
    if "NIK" in full_text:
        nik_index = full_text.find("NIK")
        data["NIK"] = full_text[nik_index+3:].split()[0]

    # Lanjutkan parsing pakai keyword atau regex

    return data

def proses_folder(folder="image"):
    hasil = []
    for nama_file in os.listdir(folder):
        if nama_file.endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(folder, nama_file)
            print(f"🔍 Memproses {nama_file}")
            data = proses_ktp(path)
            data["File"] = nama_file
            hasil.append(data)
    return hasil

def simpan_excel(data, nama_file="output_easyocr.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(nama_file, index=False)
    print(f"✅ Disimpan ke {nama_file}")

if __name__ == "__main__":
    hasil = proses_folder("image")
    simpan_excel(hasil)
