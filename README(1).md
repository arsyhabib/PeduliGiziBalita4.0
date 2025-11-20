# PeduliGiziBalita v3.3 - Flask Edition

Aplikasi pemantauan pertumbuhan anak profesional berbasis WHO Child Growth Standards 2006 dan Permenkes RI No. 2 Tahun 2020.

## 🚀 Fitur Utama

### ✅ Fitur Baru v3.3 (Flask Edition)
- **Flask Web Interface** - UI modern dengan Bootstrap 5
- **Template HTML Responsif** - Mendukung semua perangkat
- **Navigation Intuitif** - Navigasi yang mudah digunakan
- **Dashboard Interaktif** - Visualisasi data yang menarik

### ✅ Fitur v3.2
- **Mode Mudah** - Quick reference untuk range normal
- **Perpustakaan Updated** - 50+ artikel terverifikasi
- **Kalkulator Target Kejar Tumbuh** - Growth velocity monitoring profesional
- **Bug Fix** - HTML rendering di checklist wizard

### ✅ Fitur v3.1
- **YouTube Video Integration** - Video edukasi KPSP & MP-ASI
- **Dark Mode Optimization** - Kontras yang lebih baik
- **Reminder Slider** - Diubah dari menit ke jam
- **50 Artikel Indonesia** - Koleksi artikel lokal

### ✅ Fitur v3.0
- **WHO Calculator Integration** - Z-score calculation akurat
- **PDF Report Export** - Laporan profesional dengan QR code
- **KPSP Screening** - Kuesioner Pra Skrining Perkembangan
- **Growth Charts Visualization** - Grafik pertumbuhan interaktif

## 📊 Teknologi yang Digunakan

### Backend
- **Flask 2.3.3** - Web framework Python
- **WHO pygrowup** - Z-score calculator
- **NumPy 1.26.4** - Numerical computing
- **Pandas 2.2.3** - Data manipulation
- **Matplotlib 3.9.2** - Data visualization

### Frontend
- **Bootstrap 5.3.0** - CSS framework
- **Font Awesome 6.0.0** - Icons
- **Google Fonts** - Typography
- **Chart.js** - Interactive charts
- **jQuery 3.6.0** - JavaScript library

## 🛠️ Instalasi

### Persyaratan Sistem
- Python 3.10.13
- 2GB RAM (minimum)
- 1GB storage space

### Langkah Instalasi

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/peduligizibalita-flask.git
cd peduligizibalita-flask
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup WHO Calculator**
```bash
# Pastikan package pygrowup tersedia di direktori
# atau install dari source yang disediakan
```

4. **Jalankan Aplikasi**
```bash
# Untuk development
python app.py

# Untuk production dengan gunicorn
gunicorn app:app --host 0.0.0.0 --port $PORT
```

## 📁 Struktur Direktori

```
peduligizibalita-flask/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── python-version        # Python version specification
├── .gitignore            # Git ignore rules
├── README.md             # Documentation
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── dashboard.html    # Dashboard
│   ├── calculator.html   # Z-score calculator
│   ├── kpsp.html         # KPSP screening
│   ├── library.html      # Article library
│   ├── growth_tracker.html # Growth tracking
│   ├── immunization.html # Immunization schedule
│   ├── videos.html       # Educational videos
│   └── reports.html      # Reports and analytics
└── outputs/              # Generated files (PDF, charts)
```

## 🎯 Halaman yang Tersedia

### 1. **Beranda (/)**
- Overview aplikasi
- Statistik penggunaan
- Aksi cepat
- Artikel terbaru

### 2. **Dashboard (/dashboard)**
- Statistik real-time
- Grafik pertumbuhan
- Peringatan dan notifikasi
- Daftar anak

### 3. **Kalkulator Z-Score (/calculator)**
- Input data antropometri
- Perhitungan Z-Score WHO
- Klasifikasi status gizi
- Visualisasi hasil

### 4. **Skrining KPSP (/kpsp)**
- Kuesioner perkembangan anak
- Evaluasi milestone
- Rekomendasi lanjutan
- Riwayat penilaian

### 5. **Perpustakaan (/library)**
- Artikel kesehatan anak
- Filter dan pencarian
- Preview artikel
- Statistik perpustakaan

### 6. **Fitur Tambahan**
- **Pelacak Pertumbuhan** (/growth_tracker)
- **Jadwal Imunisasi** (/immunization)
- **Video Edukasi** (/videos)
- **Laporan** (/reports)

## 📊 API Endpoints

### Z-Score Calculator
```http
POST /api/calculate-zscore
Content-Type: application/json

{
    "weight": 10.5,
    "height": 78.0,
    "age_months": 18,
    "gender": "F",
    "type": "wfa"
}
```

### KPSP Evaluation
```http
POST /api/kpsp-evaluate
Content-Type: application/json

{
    "age_months": 12,
    "answers": [true, false, true, true, false]
}
```

### Growth Data
```http
GET /api/growth-data
```

### API Information
```http
GET /api/info
```

## 🎨 Desain dan UI

### Warna Utama
- **Primary**: #8B4513 (Brown)
- **Secondary**: #D2691E (Chocolate)
- **Accent**: #CD853F (Peru)
- **Success**: #28a745
- **Warning**: #ffc107
- **Danger**: #dc3545

### Font
- **Heading**: Crimson Text (serif)
- **Body**: Inter (sans-serif)

### Responsive Design
- Mobile-first approach
- Bootstrap 5 grid system
- Flexible layouts
- Touch-friendly interface

## 🔧 Konfigurasi

### Environment Variables
```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# Application Settings
APP_VERSION=3.3.0
APP_TITLE=PeduliGiziBalita
CONTACT_WA=6285888858160
BASE_URL=https://your-domain.com

# Database (jika menggunakan)
DATABASE_URL=sqlite:///app.db
```

### WHO Calculator Configuration
```python
CALC_CONFIG = {
    'adjust_height_data': False,
    'adjust_weight_scores': False,
    'include_cdc': False,
    'logger_name': 'who_calculator',
    'log_level': 'ERROR'
}
```

## 📈 Monitoring dan Analytics

### Performance Metrics
- Response time < 2 seconds
- Memory usage monitoring
- Error rate tracking
- User engagement metrics

### Health Check
```http
GET /health
```

## 🔒 Keamanan

### Security Features
- CSRF protection
- Input validation
- XSS prevention
- SQL injection prevention
- Secure headers

### Best Practices
- Environment variables for secrets
- Regular dependency updates
- Security headers
- HTTPS enforcement

## 🚀 Deployment

### Render.com
1. Connect GitHub repository
2. Set Python version to 3.10.13
3. Configure build command: `pip install -r requirements.txt`
4. Configure start command: `gunicorn app:app --host 0.0.0.0 --port $PORT`
5. Set environment variables

### Heroku
1. Create Heroku app
2. Set Python buildpack
3. Configure Procfile: `web: gunicorn app:app`
4. Set environment variables
5. Deploy

### Docker
```dockerfile
FROM python:3.10.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
```

## 📱 Mobile Support

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Mobile Features
- Touch-friendly interface
- Swipe gestures
- Optimized for small screens
- Fast loading on mobile networks

## 🤝 Kontribusi

### Cara Berkontribusi
1. Fork repository
2. Buat branch fitur
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

### Code Style
- PEP 8 untuk Python
- ESLint untuk JavaScript
- Prettier untuk HTML/CSS

## 📄 Lisensi

Educational & Healthcare Use

## 👥 Tim Pengembang

- **Habib Arsy** - FKIK Universitas Jambi
- **Kontak**: +6285888858160

## 📞 Dukungan

Untuk bantuan dan dukungan:
- WhatsApp: +6285888858160
- Email: support@peduligizibalita.id
- GitHub Issues: https://github.com/yourusername/peduligizibalita-flask/issues

## 🔄 Update dan Maintenance

### Update Schedule
- Security updates: Monthly
- Feature updates: Quarterly
- Major releases: Annually

### Changelog
- **v3.3.0** - Flask Edition dengan UI baru
- **v3.2.3** - Perpustakaan artikel updated
- **v3.2.0** - Mode mudah dan kalkulator kejar tumbuh
- **v3.1.0** - YouTube integration dan dark mode
- **v3.0.0** - WHO calculator dan PDF reports

---

**PeduliGiziBalita v3.3** - Monitoring pertumbuhan anak dengan standar WHO yang profesional dan user-friendly.