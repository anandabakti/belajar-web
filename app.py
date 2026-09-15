from flask import Flask, send_from_directory, jsonify
from datetime import datetime
import json
import os
import subprocess
import sys
import threading
import time

app = Flask(__name__)

folder_proyek = os.path.dirname(os.path.abspath(__file__))
waktu_terakhir = "Belum pernah diperbarui"

def jalankan_pengambilan():
    global waktu_terakhir

    hasil = subprocess.run(
        [sys.executable, "ambil_berita.py"],
        cwd=folder_proyek,
        capture_output=True,
        text=True,
        timeout=30
    )

    if hasil.returncode == 0:
        waktu_terakhir = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print("Berita otomatis diperbarui:", waktu_terakhir)
        return True, "Berita berhasil diperbarui."

    return False, hasil.stderr

def ambil_berita_otomatis():
    while True:
        try:
            jalankan_pengambilan()
        except Exception as error:
            print("Gagal memperbarui berita:", error)

        time.sleep(300)

@app.route("/")
def halaman_utama():
    return send_from_directory(folder_proyek, "index.html")

@app.route("/style.css")
def file_css():
    return send_from_directory(folder_proyek, "style.css")

@app.route("/api/temuan")
def temuan_otomatis():
    lokasi_file = os.path.join(folder_proyek, "isu_otomatis.json")

    if not os.path.exists(lokasi_file):
        return jsonify([])

    with open(lokasi_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    return jsonify(data)

@app.route("/api/status")
def status_sistem():
    return jsonify({
        "waktu": waktu_terakhir
    })

@app.route("/api/perbarui-berita", methods=["POST"])
def perbarui_berita():
    berhasil, pesan = jalankan_pengambilan()

    return jsonify({
        "berhasil": berhasil,
        "pesan": pesan
    })

if __name__ == "__main__":
    threading.Thread(target=ambil_berita_otomatis, daemon=True).start()
    app.run(host="127.0.0.1", port=5000)
    