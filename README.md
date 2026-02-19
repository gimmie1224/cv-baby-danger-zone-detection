👶 Baby Restricted Area Monitoring System

Proyek ini merupakan implementasi sistem monitoring area terlarang untuk bayi berbasis *computer vision* menggunakan video real-time. Sistem dirancang untuk mendeteksi pergerakan bayi melalui pendekatan pose estimation dan memberikan peringatan (alarm) ketika bayi memasuki area yang telah ditentukan sebagai zona terlarang (virtual fence).

🎯 Tujuan Sistem
* Mendeteksi keberadaan dan pose manusia menggunakan MediaPipe
* Menentukan area terlarang (virtual fence) pada frame kamera
* Menghitung jarak relatif objek terhadap area terlarang
* Mengaktifkan alarm ketika objek memasuki zona bahaya
* Menganalisis performa sistem dalam berbagai kondisi pengujian

🧠 Teknologi yang Digunakan
* Python
* OpenCV
* MediaPipe (Pose Estimation)
* Scikit-Fuzzy (Fuzzy Logic System)
* NumPy
* Requests (untuk integrasi notifikasi)
* Playsound (alarm system)

⚙️ Instalasi
1️⃣ Clone repository
- git clone https://github.com/gimmie1224/cv-baby-danger-zone-detection.git
- cd cv-baby-danger-zone-detection

2️⃣ Buat virtual environment (disarankan)
Windows:
- python -m venv venv
- venv\Scripts\activate

Mac/Linux:
- python3 -m venv venv
- source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

▶️ Cara Menjalankan Sistem
python main.py

Pastikan:
* Kamera terhubung dan berfungsi
* File alarm tersedia
* Pencahayaan cukup untuk deteksi pose

🔬 Cara Kerja Sistem
1. Kamera menangkap video secara real-time.
2. MediaPipe mendeteksi pose manusia pada frame.
3. Sistem menentukan posisi relatif terhadap virtual fence.
4. Fuzzy logic digunakan untuk menentukan tingkat bahaya.
5. Jika objek memasuki zona terlarang → alarm aktif.

⚠️ Keterbatasan Sistem
* Tidak dapat membedakan bayi dan orang dewasa.
* Cenderung mendeteksi objek manusia yang paling dominan di dalam frame.
* Perhitungan jarak berbasis proyeksi 2D (bukan jarak nyata 3D).
* Sensitif terhadap sudut kamera dan kondisi pencahayaan.
* Virtual fence bersifat statis..



