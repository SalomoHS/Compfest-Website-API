<p align="center">
  <h3 align="center">Kota Berbicara - Website Backend</h3>
</p>

<p align="center">
  <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&center=true&vCenter=true&width=435&lines=Dengarkan+kota+anda+berbicara" alt="Typing SVG" /></a>
</p>

<p align="center">
  Platform inovatif yang menghubungkan warga dengan kota mereka melalui podcast informatif yang dihasilkan oleh AI. Kami berkomitmen untuk menyediakan informasi terkini tentang pembangunan kota cerdas di Indonesia
</p>

<p align="center">
    <img alt="Langchain" src="https://custom-icon-badges.demolab.com/badge/Langgraph-2EAD33?logo=langchain&logoColor=fff"/>
  <img alt="FastApi" src="https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white"/>
   <img alt="ElevenLabs" src="https://img.shields.io/badge/ElevenLabs-black.svg?logo=elevenlabs&logoColor=white"/>
  <img alt="Gemini" src="https://img.shields.io/badge/Google%20Gemini-8E75B2.svg?logo=google%20gemini&logoColor=white"/>
   <img alt="Supabase" src="https://custom-icon-badges.demolab.com/badge/Supabase-white?logo=supabase&logoColor=2EAD33"/>
   <img alt="Shotstack" src="https://img.shields.io/badge/Shotstack-22ADF6?&logo=InfluxDB&logoColor=white"/>
</p>

<p align="center">
    <a href="https://compfest-podcast-generator-frontend.vercel.app/">
      <img src="https://custom-icon-badges.demolab.com/badge/-Click%20Me%20to%20Visit%20Website-palegreen?style=for-the-badge&logoColor=white" title="Kota Berbicara Website's" alt="Kota Berbicara Website's"/></a>
</p>
<p align="center">
  <a href="https://youtu.be/3oToZepB7tM">
      <img src="https://custom-icon-badges.demolab.com/badge/-Video%20Demo-B71C1C?style=for-the-badge&logo=YouTube&logoColor=white" title="Demo video" alt="Demo Video"/></a>
  <a href="https://www.tiktok.com/@kotaberbicara">
      <img src="https://custom-icon-badges.demolab.com/badge/-Kota%20Berbicara%20Tiktok-black?style=for-the-badge&logo=TIktok&logoColor=white" title="Kota Berbicara tiktok's" alt="Kota Berbicara Titkok's"/></a>
</p>

--- 

### Deskripsi Tugas
Backend ini bertugas untuk menangani proses publikasi konten podcast "Kota Berbicara". Di dalam backend ini terintegrasi ke sistem eksternal seperti elevenlabs, supabase, shotstack, dan make.com. Backend ini akan berjalan jika mendapat request dari make.com. Dimana Make.com akan request sesuai jadwal yang sudah ditentukan oleh pengembang.

---

### Use Case
1. **Mengirim data podcast ke website**
2. **Membuat naskah podcast**
3. **Membuat podcast audio**
4. **Membaca data speaker dan topik podcast di database**
5. **Memiliki akses ke storage bucket untuk menyimpan dan mendapatkan audio podcast**
7. **Menambahkan background musik pada audio podcast**

--- 

### Fitur
1. **Terhubung ke sistem eksternal (elevenlabs, supabase, shotstack, dan make.com)** -- Backend terhubung ke berbagai sistem eksternal untuk mendukung publikasi konten "Kota Berbicara"

---

### Sistem eksternal 
1. `Supabase` -- Sistem yang menyediakan layanan database berbasis PostgreSQL dan storage bucket.
2. `Elevenlabs` -- Sistem yang menyediakan layanan membuat audio sintetis berbasis AI.
3. `Shotstack` -- Sistem yang menyediakan layanan editing video berbasis API.

---

### 📄 Deskripsi File
- 📄 `agent.py` – Berisikan AI Agent yang dibutuhkan untuk mendukung workflow.  
- 📄 `app.py` – Menangani rute API dan pemrosesan permintaan.  
- 📄 `elevenlabsClient.py` – Klien untuk berinteraksi dengan ElevenLabs PythonSDK.  
- 📄 `flow.py` – Workflow, dibangun dengan framework langgraph.  
- 📄 `prompt.txt` – Berisi template prompt atau instruksi statis untuk AI agent membuat naskah podcast.
- 📄 `prompt-1speaker.txt` – Berisi template prompt atau instruksi statis untuk AI agent membuat naskah podcast 1 speaker.  
- 📄 `requirements.txt` – Daftar dependensi Python yang dibutuhkan untuk menjalankan proyek.  
- 📄 `supabaseClient.py` – Klien untuk berinteraksi dengan Supabase PythonSDK.  
- 📄 `tools.py` – Tools umum dan fungsi utilitas yang digunakan di AI agent yang digunakan.

---

### Kontributor
<p>
  <a href="https://www.linkedin.com/in/salomohendriansudjono/">
    <img alt="Salomo Hendrian Sudjono" title="Salomo Hendrian Sudjono" src="https://custom-icon-badges.demolab.com/badge/-Salomo%20Hendrian%20Sudjono-blue?style=for-the-badge&logo=person-fill&logoColor=white"/>
  </a>
  <a href="https://id.linkedin.com/in/matthew-lefrandt-6578a1298/">
    <img alt="Matthew Lefrandt" title="Matthew Lefrandt" src="https://custom-icon-badges.demolab.com/badge/-Matthew%20Lefrandt-blue?style=for-the-badge&logo=person-fill&logoColor=white"/>
  </a>
</p>
