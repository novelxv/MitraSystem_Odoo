# MitraSystem - Modul Manajemen Proyek Odoo

**MitraSystem** adalah modul kustom Odoo berbasis Community Edition untuk mengelola proyek, penjadwalan, staf, laporan, evaluasi, handover tugas, dan komplain secara terintegrasi. Dirancang untuk organisasi yang membutuhkan alur kerja proyek yang efisien dan kolaboratif.

---

## 🧩 Fitur Utama

- **Manajemen Proyek:** Tambah dan kelola proyek dengan penanggung jawab, klien, status, dan progres.
- **Penjadwalan Tugas:** Buat dan kelola tugas proyek beserta jadwal pengerjaannya dengan tampilan kanban dan kalender.
- **Handover Tugas:** Serahkan tugas antar staf dan pantau statusnya.
- **Manajemen Staf:** Kelola informasi staf termasuk peran dan status aktif/nonaktif.
- **Evaluasi Proyek:** Catat evaluasi proyek berdasarkan waktu, anggaran, dan kualitas.
- **Laporan Proyek:** Simpan dan unggah laporan proyek berkala (PDF, XLSX, PPTX).
- **Komplain Klien:** Catat dan tangani komplain dari klien proyek.
- **Dashboard:** Ringkasan proyek berjalan, selesai, dan yang perlu perhatian.

---

## 👥 Role & Akses

| Role              | Hak Akses Utama                                                                 |
|-------------------|---------------------------------------------------------------------------------|
| Admin Sistem      | CRUD semua data, termasuk staf, proyek, laporan, komplain                      |
| PIC Proyek        | Melihat proyek yang ditugaskan, jadwal, handover, evaluasi, komplain            |
| Manajemen         | Melihat & membuat evaluasi, melihat laporan                                     |
| Manajemen Senior  | Melihat staf, melihat laporan & evaluasi                                        |

---

## ⚙️ Instalasi

1. Clone atau salin folder modul ke direktori `addons` lokal Odoo:

   ```bash
   git clone https://github.com/novelxv/mitrasystem_odoo.git
   ```

2. Tambahkan jalur modul ke konfigurasi Odoo (`odoo.conf`):

   ```ini
   [options]
   addons_path = /path/to/your/addons, /path/to/mitrasystem_odoo
   ```

3. Restart Odoo server:

   ```bash
   sudo systemctl restart odoo
   ```

   atau

   ```bash
   ./odoo-bin -c /path/to/your/odoo.conf
   ```

4. Aktifkan mode pengembang di Odoo.

5. Instal MitraSystem melalui antarmuka Odoo:

   - Buka menu "Aplikasi".
   - Cari "MitraSystem".
   - Klik "Instal".

---

## 🚀 Cara Penggunaan

1. **Login ke Odoo**
   - Gunakan akun yang sesuai dengan role Anda (Admin Sistem, PIC Proyek, dll).

2. **Manajemen Proyek**
   - Tambahkan proyek baru melalui menu "Proyek".
   - Tetapkan penanggung jawab, klien, dan detail lainnya.

3. **Penjadwalan Tugas**
   - Buat jadwal tugas melalui menu "Penjadwalan".
   - Tetapkan staf atau pengguna yang bertanggung jawab.

4. **Handover Tugas**
   - Gunakan menu "Handover Tugas" untuk menyerahkan tugas ke staf lain.
   - Pantau status handover hingga selesai.

5. **Evaluasi Proyek**
   - Catat evaluasi proyek melalui menu "Evaluasi".
   - Tambahkan catatan terkait waktu, anggaran, dan kualitas.

6. **Laporan Proyek**
   - Unggah laporan proyek berkala melalui menu "Laporan".

7. **Komplain Klien**
   - Catat komplain klien melalui menu "Komplain".
   - Tindak lanjuti komplain hingga selesai.

8. **Dashboard**
   - Gunakan dashboard untuk melihat ringkasan proyek berjalan, selesai, dan yang membutuhkan perhatian.

---

## 🛠️ Pengembangan & Kontribusi

1. **Struktur Modul**
   - `models/`: Berisi definisi model Odoo.
   - `views/`: Berisi definisi tampilan (form, list, kanban, dll).
   - `security/`: Berisi aturan akses dan grup pengguna.
   - `data/`: Berisi data awal seperti sequence.

2. **Menambahkan Fitur Baru**
   - Tambahkan model baru di folder `models/`.
   - Tambahkan tampilan baru di folder `views/`.
   - Perbarui file `__manifest__.py` untuk mendaftarkan model dan tampilan baru.

3. **Kontribusi**
   - Fork repository ini.
   - Buat branch baru untuk fitur atau perbaikan Anda.
   - Kirim pull request dengan deskripsi yang jelas.

---