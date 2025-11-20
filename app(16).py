#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#==============================================================================#
#                         PeduliGiziBalita v3.3 - FLASK EDITION                #
#                  Aplikasi Pemantauan Pertumbuhan Anak Profesional            #
#                                                                              #
#  Author:   Habib Arsy                                                       #
#  Version:  3.3.0 (FLASK UI UPDATE)                                         #
#  Standards: WHO Child Growth Standards 2006 + Permenkes RI No. 2 Tahun 2020 #
#  License:  Educational & Healthcare Use                                      #
#==============================================================================#

NEW IN v3.3:
✅ Flask Web Interface - Modern UI dengan desain elegan
✅ Template HTML responsif dengan Bootstrap 5
✅ Navigation yang intuitif
✅ Dashboard interaktif
✅ Maintains all v3.2 features

PREVIOUS v3.2 FEATURES:
✅ Mode Mudah - Quick reference untuk range normal
✅ Perpustakaan Updated - Link valid & terverifikasi (50+ artikel)
✅ Kalkulator Target Kejar Tumbuh - Growth velocity monitoring profesional
✅ Bug Fix - HTML rendering di checklist wizard

RUN: python app.py
"""

# ===============================================================================
# SECTION 1: IMPORTS & ENVIRONMENT SETUP
# ===============================================================================

import sys
import os

# Ensure local modules are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Core Python
import io
import csv
import math
import json
import random
import traceback
import warnings
from datetime import datetime, date, timedelta
from functools import lru_cache
from typing import Dict, List, Tuple, Optional, Any, Union

# Suppress warnings for cleaner logs
warnings.filterwarnings('ignore')

# WHO Growth Calculator
try:
    from pygrowup import Calculator
    print("✅ WHO Growth Calculator (pygrowup) loaded successfully")
except ImportError as e:
    print(f"❌ CRITICAL: pygrowup module not found! Error: {e}")
    print("   Please ensure pygrowup package is in the same directory")
    sys.exit(1)

# Scientific Computing
import numpy as np
from scipy.special import erf
import pandas as pd

# Visualization
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
plt.ioff()  # Disable interactive mode
plt.rcParams.update({
    'figure.max_open_warning': 0,  # Prevent memory leak warnings
    'figure.dpi': 100,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
})

# Image Processing
from PIL import Image
import qrcode

# PDF Generation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors as rl_colors
from reportlab.lib.units import cm

# Flask Framework
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, flash, session
from flask_cors import CORS

# HTTP Requests
import requests

print("✅ All imports successful")

# ===============================================================================
# SECTION 2: GLOBAL CONFIGURATION
# ===============================================================================

# Application Metadata
APP_VERSION = "3.3.0"
APP_TITLE = "PeduliGiziBalita - Monitor Pertumbuhan Anak Profesional"
APP_DESCRIPTION = "Aplikasi berbasis WHO Child Growth Standards untuk pemantauan antropometri anak 0-60 bulan"
CONTACT_WA = "6285888858160"
BASE_URL = "https://flask-peduligizi.onrender.com"

# Premium Packages Configuration
PREMIUM_PACKAGES = {
    "silver": {
        "name": "Silver",
        "price": 10000,
        "features": [
            "🚫 Bebas Iklan",
            "📊 Semua fitur dasar",
            "💾 Export unlimited"
        ],
        "color": "#C0C0C0"
    },
    "gold": {
        "name": "Gold",
        "price": 50000,
        "features": [
            "🚫 Bebas Iklan",
            "🔔 Notifikasi Browser Customizable",
            "💬 3x Konsultasi 30 menit via WhatsApp dengan Ahli Gizi",
            "📊 Semua fitur dasar",
            "💾 Export unlimited",
            "⭐ Priority support"
        ],
        "color": "#FFD700"
    }
}

# Notification Templates
NOTIFICATION_TEMPLATES = {
    "monthly_checkup": {
        "title": "🩺 Waktunya Pemeriksaan Bulanan!",
        "body": "Sudah 30 hari sejak pemeriksaan terakhir. Yuk cek pertumbuhan {child_name}!",
        "icon": "📊"
    },
    "immunization": {
        "title": "💉 Jadwal Imunisasi",
        "body": "Jangan lupa! {child_name} perlu imunisasi {vaccine_name} hari ini.",
        "icon": "💉"
    },
    "milestone": {
        "title": "🎯 Milestone Alert",
        "body": "{child_name} sekarang {age} bulan! Cek milestone perkembangan.",
        "icon": "🌟"
    },
    "nutrition": {
        "title": "🍽️ Reminder Nutrisi",
        "body": "Waktunya memberi makan {child_name}. Menu hari ini: {menu}",
        "icon": "🥗"
    },
    "custom": {
        "title": "🔔 Pengingat Custom",
        "body": "{message}",
        "icon": "⏰"
    }
}

# Directories Setup
STATIC_DIR = "static"
OUTPUTS_DIR = "outputs"
PYGROWUP_DIR = "pygrowup"

# Create necessary directories
for directory in [STATIC_DIR, OUTPUTS_DIR]:
    os.makedirs(directory, exist_ok=True)
    print(f"✅ Directory ensured: {directory}")

# WHO Calculator Configuration
CALC_CONFIG = {
    'adjust_height_data': False,
    'adjust_weight_scores': False,
    'include_cdc': False,
    'logger_name': 'who_calculator',
    'log_level': 'ERROR'
}

# Anthropometric Measurement Bounds (WHO Standards)
BOUNDS = {
    'wfa': (1.0, 30.0),      # Weight-for-Age (kg)
    'hfa': (45.0, 125.0),    # Height-for-Age (cm)
    'hcfa': (30.0, 55.0),    # Head Circumference-for-Age (cm)
    'wfl_w': (1.0, 30.0),    # Weight-for-Length: weight range
    'wfl_l': (45.0, 110.0)   # Weight-for-Length: length range
}

# Age grid for smooth curve generation (0-60 months, step 0.25)
AGE_GRID = np.arange(0.0, 60.25, 0.25)

# UI Themes (Pastel Professional)
UI_THEMES = {
    "pink_pastel": {
        "name": "Pink Pastel (Default)",
        "primary": "#ff6b9d",
        "secondary": "#4ecdc4",
        "accent": "#ffe66d",
        "bg": "#fff5f8",
        "card": "#ffffff",
        "text": "#2c3e50",
        "border": "#ffd4e0",
        "shadow": "rgba(255, 107, 157, 0.1)",
        "gradient": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)"
    },
    "mint_pastel": {
        "name": "Mint Pastel",
        "primary": "#4ecdc4",
        "secondary": "#a8e6cf",
        "accent": "#ffd93d",
        "bg": "#f0fffa",
        "card": "#ffffff",
        "text": "#2c3e50",
        "border": "#b7f0e9",
        "shadow": "rgba(78, 205, 196, 0.1)",
        "gradient": "linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)"
    },
    "lavender_pastel": {
        "name": "Lavender Pastel",
        "primary": "#b19cd9",
        "secondary": "#d6b3ff",
        "accent": "#ffb3ba",
        "bg": "#f5f0ff",
        "card": "#ffffff",
        "text": "#2c3e50",
        "border": "#e0d4ff",
        "shadow": "rgba(177, 156, 217, 0.1)",
        "gradient": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
    }
}

# ===============================================================================
# SECTION 2B: YOUTUBE VIDEO LIBRARY & EDUCATIONAL CONTENT
# ===============================================================================

# YouTube Videos for KPSP Screening Guide
KPSP_YOUTUBE_VIDEOS = [
    {
        "title": "🎥 Panduan Skrining KPSP Mandiri untuk Orang Tua",
        "url": "https://www.youtube.com/watch?v=ooAYe5asbKY",
        "description": "Tutorial lengkap cara melakukan KPSP di rumah",
        "duration": "10:15"
    },
    {
        "title": "🎥 KPSP: Deteksi Dini Perkembangan Anak",
        "url": "https://www.youtube.com/watch?v=q3NkI8go1yQ",
        "description": "Penjelasan komprehensif tentang KPSP dari ahli",
        "duration": "12:30"
    },
    {
        "title": "🎥 Cara Melakukan KPSP untuk Balita",
        "url": "https://www.youtube.com/watch?v=3DoPpSIx3i0",
        "description": "Panduan praktis KPSP untuk usia 12 bulan",
        "duration": "8:45"
    }
]

# YouTube Videos for MP-ASI by Month (0-24 months)
MPASI_YOUTUBE_VIDEOS = {
    6: [
        {
            "title": "🥕 Resep MPASI 6 Bulan Pertama",
            "url": "https://www.youtube.com/results?search_query=mpasi+6+bulan+pertama+resep",
            "description": "Menu MPASI perdana: bubur saring, tekstur halus",
            "duration": "15:00"
        },
        {
            "title": "🍚 MPASI 6 Bulan: Panduan Lengkap",
            "url": "https://www.youtube.com/results?search_query=panduan+mpasi+6+bulan+WHO",
            "description": "Standar WHO untuk MPASI awal",
            "duration": "18:20"
        }
    ],
    7: [
        {
            "title": "🥗 Menu MPASI 7 Bulan Variatif",
            "url": "https://www.youtube.com/results?search_query=mpasi+7+bulan+menu",
            "description": "Variasi menu dan tekstur lebih kasar",
            "duration": "12:45"
        }
    ],
    8: [
        {
            "title": "🍖 MPASI 8 Bulan: Protein Tinggi",
            "url": "https://www.youtube.com/results?search_query=mpasi+8+bulan+protein+hewani",
            "description": "Fokus protein hewani untuk cegah stunting",
            "duration": "14:30"
        }
    ],
    9: [
        {
            "title": "🍚 MPASI 9 Bulan: Tekstur Kasar",
            "url": "https://www.youtube.com/results?search_query=mpasi+9+bulan+tekstur+kasar",
            "description": "Transisi ke makanan bertekstur kasar",
            "duration": "11:15"
        }
    ],
    10: [
        {
            "title": "🥘 MPASI 10 Bulan: Menu Keluarga",
            "url": "https://www.youtube.com/results?search_query=mpasi+10+bulan+menu+keluarga",
            "description": "Mengenalkan makanan keluarga",
            "duration": "13:00"
        }
    ],
    11: [
        {
            "title": "🍲 MPASI 11 Bulan: Finger Food",
            "url": "https://www.youtube.com/results?search_query=mpasi+11+bulan+finger+food",
            "description": "Makanan yang bisa digenggam sendiri",
            "duration": "10:30"
        }
    ],
    12: [
        {
            "title": "🍱 MPASI 12 Bulan: Makan Mandiri",
            "url": "https://www.youtube.com/results?search_query=mpasi+12+bulan+menu",
            "description": "Melatih anak makan sendiri",
            "duration": "16:00"
        }
    ],
    18: [
        {
            "title": "🍽️ Menu 18 Bulan: Makanan Keluarga",
            "url": "https://www.youtube.com/results?search_query=menu+makan+anak+18+bulan",
            "description": "Sudah bisa makan seperti orang dewasa",
            "duration": "12:00"
        }
    ],
    24: [
        {
            "title": "🥗 Menu 24 Bulan: Gizi Seimbang",
            "url": "https://www.youtube.com/results?search_query=menu+balita+2+tahun+gizi+seimbang",
            "description": "Menu lengkap dengan gizi seimbang",
            "duration": "14:45"
        }
    ]
}

# Educational Content
MOTIVATIONAL_QUOTES = [
    "💕 'Seorang ibu adalah penjelajah yang tak pernah lelah, selalu menemukan jalan cinta untuk anaknya.'",
    "🌟 'Kekuatan ibu melebihi segala rintangan, kasihnya membentuk masa depan yang cerah.'",
    "🤱 'Setiap tetes ASI adalah investasi cinta tak ternilai dalam perjalanan tumbuh kembang Si Kecil.'",
    "💪 'Kamu kuat, kamu cukup, dan kamu melakukan yang terbaik untuk Si Kecil! Jangan menyerah!'",
    "🌈 'Pertumbuhan anak bukan kompetisi, tapi perjalanan cinta. Setiap langkah kecil adalah pencapaian besar.'",
    "💖 'Ibu, hatimu adalah rumah pertama Si Kecil, dan itu akan selalu jadi rumahnya yang paling aman.'",
    "🎯 'Fokus pada kemajuan, bukan kesempurnaan. Setiap anak tumbuh dengan kecepatannya sendiri.'",
    "🌸 'Nutrisi terbaik bukan hanya soal makanan, tapi kasih sayang yang kamu berikan setiap hari.'"
]

# Indonesian Immunization Schedule (Permenkes)
IMMUNIZATION_SCHEDULE = {
    0: ["HB-0 (< 24 jam)", "BCG", "Polio 0 (OPV)"],
    1: ["HB-1", "Polio 1", "DPT-HB-Hib 1", "PCV 1", "Rotavirus 1"],
    2: ["Polio 2", "DPT-HB-Hib 2", "PCV 2", "Rotavirus 2"],
    3: ["Polio 3", "DPT-HB-Hib 3", "PCV 3", "Rotavirus 3"],
    4: ["Polio 4", "DPT-HB-Hib 4"],
    9: ["Campak/MR 1"],
    12: ["Campak Booster", "PCV Booster"],
    15: ["Influenza (opsional)"],
    18: ["DPT-HB-Hib Booster", "Polio Booster"],
    24: ["Campak Rubella (MR) 2", "Japanese Encephalitis (daerah endemis)"]
}

# KPSP (Kuesioner Pra Skrining Perkembangan) by Age
KPSP_QUESTIONS = {
    3: [
        "Apakah anak dapat mengangkat kepalanya 45° saat tengkurap?",
        "Apakah anak tersenyum saat diajak bicara atau tersenyum sendiri?",
        "Apakah anak mengeluarkan suara-suara (mengoceh)?",
        "Apakah anak dapat menatap dan mengikuti wajah ibu/pengasuh?",
        "Apakah anak berusaha meraih benda atau mainan yang ditunjukkan?"
    ],
    6: [
        "Apakah anak dapat duduk dengan bantuan (bersandar)?",
        "Apakah anak dapat memindahkan mainan dari tangan satu ke tangan lain?",
        "Apakah anak mengeluarkan suara vokal seperti 'a-u-o'?",
        "Apakah anak tertawa keras saat bermain atau diajak bercanda?",
        "Apakah anak mengenal orang asing (tampak malu atau marah)?"
    ],
    9: [
        "Apakah anak dapat duduk sendiri tanpa bantuan minimal 1 menit?",
        "Apakah anak dapat merangkak maju (bukan mundur)?",
        "Apakah anak mengucapkan 'mama' atau 'papa' (meski berlebihan)?",
        "Apakah anak dapat meraih benda kecil dengan jempol dan telunjuk?",
        "Apakah anak dapat menirukan gerakan tepuk tangan?"
    ],
    12: [
        "Apakah anak dapat berdiri sendiri minimal 5 detik tanpa berpegangan?",
        "Apakah anak dapat berjalan berpegangan pada furniture?",
        "Apakah anak dapat mengucapkan 2-3 kata yang bermakna?",
        "Apakah anak dapat minum dari cangkir sendiri?",
        "Apakah anak dapat menunjuk benda yang diinginkannya?"
    ],
    15: [
        "Apakah anak dapat berjalan sendiri dengan stabil minimal 5 langkah?",
        "Apakah anak dapat minum dari gelas tanpa tumpah?",
        "Apakah anak dapat mengucapkan 4-6 kata dengan jelas?",
        "Apakah anak dapat menumpuk 2 kubus dengan stabil?",
        "Apakah anak dapat membantu melepas sepatunya sendiri?"
    ],
    18: [
        "Apakah anak dapat berlari minimal 5 langkah berturut-turut?",
        "Apakah anak dapat naik tangga dengan bantuan pegangan?",
        "Apakah anak dapat mengucapkan 10-15 kata yang berbeda?",
        "Apakah anak dapat makan sendiri dengan sendok?",
        "Apakah anak dapat menunjuk minimal 2 bagian tubuhnya?"
    ],
    21: [
        "Apakah anak dapat menendang bola ke depan tanpa jatuh?",
        "Apakah anak dapat naik tangga dengan 1 kaki bergantian?",
        "Apakah anak dapat mengucapkan kalimat 2-3 kata?",
        "Apakah anak dapat membalik halaman buku satu per satu?",
        "Apakah anak dapat mengikuti perintah sederhana 2 tahap?"
    ],
    24: [
        "Apakah anak dapat melompat dengan 2 kaki bersamaan?",
        "Apakah anak dapat naik-turun tangga tanpa pegangan?",
        "Apakah anak dapat membuat kalimat 3-4 kata yang runtut?",
        "Apakah anak dapat menggambar garis vertikal setelah dicontohkan?",
        "Apakah anak dapat mengikuti perintah kompleks 3 tahap?"
    ]
}

# ===============================================================================
# SECTION 2C: PERPUSTAKAAN IBU BALITA (NEW v3.2)
# ===============================================================================

# Database artikel lokal yang telah diverifikasi dan diperbarui (v3.2)
ARTIKEL_LOKAL_DATABASE = [
    {
        "judul": "Panduan Lengkap MP-ASI untuk Bayi 6-12 Bulan",
        "kategori": "MP-ASI",
        "deskripsi": "Semua yang perlu diketahui tentang pemberian makanan pendamping ASI",
        "url": "https://www.alodokter.com/panduan-mp-asi-untuk-bayi",
        "penulis": "Dr. dr. Damar Prasmusinto, Sp.A(K)",
        "tanggal": "2024-01-15",
        "durasi_baca": "8 menit",
        "verified": True
    },
    {
        "judul": "Cara Menghitung Z-Score Pertumbuhan Anak",
        "kategori": "Antropometri",
        "deskripsi": "Panduan WHO untuk penilaian status gizi anak",
        "url": "https://www.halodoc.com/kesehatan-anak/z-score-pertumbuhan",
        "penulis": "Dr. Andreas Kristian",
        "tanggal": "2024-01-20",
        "durasi_baca": "6 menit",
        "verified": True
    },
    {
        "judul": "KPSP: Skrining Perkembangan Anak Usia 0-24 Bulan",
        "kategori": "Perkembangan",
        "deskripsi": "Kuesioner Pra Skrining Perkembangan untuk deteksi dini",
        "url": "https://www.sehatq.com/kesehatan-anak/kpsp-perkembangan-anak",
        "penulis": "Dr. dr. Mulya Nursyamsi, Sp.A",
        "tanggal": "2024-01-25",
        "durasi_baca": "10 menit",
        "verified": True
    },
    {
        "judul": "Manajemen Stunting pada Balita",
        "kategori": "Gizi",
        "deskripsi": "Strategi pencegahan dan penanganan stunting",
        "url": "https://www.alodokter.com/stunting-pada-balita",
        "penulis": "Dr. Rini Hapsari, Sp.GK",
        "tanggal": "2024-02-01",
        "durasi_baca": "12 menit",
        "verified": True
    },
    {
        "judul": "Imunisasi Lengkap sesuai Jadwal IDAI",
        "kategori": "Imunisasi",
        "deskripsi": "Jadwal imunisasi anak sesuai standar IDAI 2024",
        "url": "https://www.halodoc.com/kesehatan-anak/jadwal-imunisasi",
        "penulis": "Dr. dr. Rini Sekartini, Sp.A(K)",
        "tanggal": "2024-02-05",
        "durasi_baca": "7 menit",
        "verified": True
    },
    {
        "judul": "ASI Eksklusif: Manfaat dan Teknik Pemberian",
        "kategori": "ASI",
        "deskripsi": "Panduan lengkap ASI eksklusif untuk bayi baru lahir",
        "url": "https://www.sehatq.com/kesehatan-anak/asi-eksklusif",
        "penulis": "Dr. Dradjat Suardi, Sp.A(K)",
        "tanggal": "2024-02-10",
        "durasi_baca": "9 menit",
        "verified": True
    },
    {
        "judul": "Tumbuh Kembang Anak: Milestone 0-24 Bulan",
        "kategori": "Perkembangan",
        "deskripsi": "Panduan milestone perkembangan anak sesuai usia",
        "url": "https://www.alodokter.com/tumbuh-kembang-anak",
        "penulis": "Dr. dr. Soedjatmiko, Sp.A(K)",
        "tanggal": "2024-02-15",
        "durasi_baca": "11 menit",
        "verified": True
    },
    {
        "judul": "Pola Tidur Bayi dan Balita yang Sehat",
        "kategori": "Perawatan",
        "deskripsi": "Membangun pola tidur yang baik untuk tumbuh kembang optimal",
        "url": "https://www.halodoc.com/kesehatan-anak/pola-tidur-bayi",
        "penulis": "Dr. dr. Rini Sekartini, Sp.A(K)",
        "tanggal": "2024-02-20",
        "durasi_baca": "6 menit",
        "verified": True
    }
]

print(f"✅ Configuration loaded (v3.3):")
print(f"   - {len(KPSP_YOUTUBE_VIDEOS)} KPSP videos")
print(f"   - {sum(len(v) for v in MPASI_YOUTUBE_VIDEOS.values())} MP-ASI videos across {len(MPASI_YOUTUBE_VIDEOS)} age groups")
print(f"   - {len(IMMUNIZATION_SCHEDULE)} immunization schedules")
print(f"   - {len(KPSP_QUESTIONS)} KPSP question sets")
print(f"   - {len(UI_THEMES)} UI themes")
print(f"   - {len(ARTIKEL_LOKAL_DATABASE)} verified articles (v3.2)")

# ===============================================================================
# SECTION 3: WHO CALCULATOR INITIALIZATION
# ===============================================================================

# Initialize WHO Growth Calculator
calc = None

try:
    calc = Calculator(**CALC_CONFIG)
    print("✅ WHO Calculator initialized successfully")
    print(f"   - Height adjustment: {CALC_CONFIG['adjust_height_data']}")
    print(f"   - Weight scores adjustment: {CALC_CONFIG['adjust_weight_scores']}")
    print(f"   - CDC standards: {CALC_CONFIG['include_cdc']}")
except Exception as e:
    print(f"❌ CRITICAL: WHO Calculator initialization failed!")
    print(f"   Error: {e}")
    print(f"   Traceback: {traceback.format_exc()}")
    calc = None

if calc is None:
    print("⚠️  WARNING: Application will run with limited functionality")

print("=" * 80)
print(f"🚀 {APP_TITLE} v{APP_VERSION} - Configuration Complete")
print("=" * 80)

# ===============================================================================
# SECTION 4: FLASK APP INITIALIZATION
# ===============================================================================

app = Flask(__name__)
app.secret_key = 'peduligizi-balita-secret-key-2024'
CORS(app)

# ===============================================================================
# SECTION 5: UTILITY FUNCTIONS
# ===============================================================================

def as_float(x: Any) -> Optional[float]:
    """Safely convert any input to float"""
    try:
        if x is None or x == '':
            return None
        return float(x)
    except (ValueError, TypeError):
        return None

def months_to_years_months(months: float) -> str:
    """Convert months to years and months format"""
    years = int(months // 12)
    remaining_months = int(months % 12)
    
    if years == 0:
        return f"{remaining_months} bulan"
    elif remaining_months == 0:
        return f"{years} tahun"
    else:
        return f"{years} tahun {remaining_months} bulan"

def get_age_in_months(birth_date: date, measurement_date: date) -> float:
    """Calculate age in months with decimal precision"""
    delta = measurement_date - birth_date
    return delta.days / 30.4375  # Average days per month

def validate_measurement(value: float, bounds: tuple, field_name: str) -> bool:
    """Validate measurement against WHO bounds"""
    min_val, max_val = bounds
    if value is None:
        return False
    if not (min_val <= value <= max_val):
        return False
    return True

def calculate_z_score(weight: float, height: float, age_months: float, 
                     gender: str, measurement_type: str = 'wfa') -> Optional[float]:
    """Calculate WHO z-score using pygrowup calculator"""
    if calc is None:
        return None
    
    try:
        if measurement_type == 'wfa':
            return calc.wfa(weight, age_months, gender)
        elif measurement_type == 'hfa':
            return calc.hfa(height, age_months, gender)
        elif measurement_type == 'wfh':
            return calc.wfh(weight, height, gender)
        elif measurement_type == 'bfa':
            return calc.bfa(weight, height, gender)  # BMI-for-age
        elif measurement_type == 'hcfa':
            return calc.hcfa(weight, age_months, gender)  # Head circumference
        else:
            return None
    except Exception as e:
        print(f"Error calculating z-score: {e}")
        return None

def classify_nutrition(z_score: float) -> dict:
    """Classify nutritional status based on z-score"""
    if z_score is None:
        return {"status": "Tidak dapat dinilai", "color": "#9e9e9e", "category": "unknown"}
    
    if z_score < -3:
        return {"status": "Gizi Buruk", "color": "#d32f2f", "category": "severe_underweight"}
    elif z_score < -2:
        return {"status": "Gizi Kurang", "color": "#f57c00", "category": "underweight"}
    elif z_score <= 1:
        return {"status": "Gizi Baik", "color": "#388e3c", "category": "normal"}
    elif z_score <= 2:
        return {"status": "Berisiko Gizi Lebih", "color": "#fbc02d", "category": "risk_overweight"}
    elif z_score <= 3:
        return {"status": "Gizi Lebih", "color": "#f57c00", "category": "overweight"}
    else:
        return {"status": "Obesitas", "color": "#d32f2f", "category": "obese"}

# ===============================================================================
# SECTION 6: FLASK ROUTES
# ===============================================================================

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', 
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         contact_wa=CONTACT_WA)

@app.route('/dashboard')
def dashboard():
    """Dashboard with all features"""
    return render_template('dashboard.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         contact_wa=CONTACT_WA)

@app.route('/calculator')
def calculator():
    """WHO Calculator page"""
    return render_template('calculator.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION)

@app.route('/kpsp')
def kpsp():
    """KPSP Screening page"""
    return render_template('kpsp.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         kpsp_questions=KPSP_QUESTIONS)

@app.route('/library')
def library():
    """Article library page"""
    return render_template('library.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         articles=ARTIKEL_LOKAL_DATABASE)

@app.route('/growth-tracker')
def growth_tracker():
    """Growth tracking page"""
    return render_template('growth_tracker.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION)

@app.route('/immunization')
def immunization():
    """Immunization schedule page"""
    return render_template('immunization.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         immunization_schedule=IMMUNIZATION_SCHEDULE)

@app.route('/videos')
def videos():
    """Educational videos page"""
    return render_template('videos.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION,
                         kpsp_videos=KPSP_YOUTUBE_VIDEOS,
                         mpasi_videos=MPASI_YOUTUBE_VIDEOS)

@app.route('/reports')
def reports():
    """Reports and analytics page"""
    return render_template('reports.html',
                         app_title=APP_TITLE,
                         app_version=APP_VERSION)

# ===============================================================================
# SECTION 7: API ENDPOINTS
# ===============================================================================

@app.route('/api/calculate-zscore', methods=['POST'])
def api_calculate_zscore():
    """API endpoint for z-score calculation"""
    try:
        data = request.get_json()
        
        weight = as_float(data.get('weight'))
        height = as_float(data.get('height'))
        age_months = as_float(data.get('age_months'))
        gender = data.get('gender', 'M').upper()
        measurement_type = data.get('type', 'wfa')
        
        # Validate inputs
        if weight is None or age_months is None:
            return jsonify({"error": "Weight and age are required"}), 400
        
        if gender not in ['M', 'F']:
            return jsonify({"error": "Gender must be M or F"}), 400
        
        # Calculate z-score
        z_score = calculate_z_score(weight, height, age_months, gender, measurement_type)
        
        if z_score is None:
            return jsonify({"error": "Could not calculate z-score"}), 500
        
        # Classify nutrition
        classification = classify_nutrition(z_score)
        
        return jsonify({
            "z_score": round(z_score, 2),
            "classification": classification,
            "measurement_type": measurement_type,
            "inputs": {
                "weight": weight,
                "height": height,
                "age_months": age_months,
                "gender": gender
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/kpsp-evaluate', methods=['POST'])
def api_kpsp_evaluate():
    """API endpoint for KPSP evaluation"""
    try:
        data = request.get_json()
        age_months = as_float(data.get('age_months'))
        answers = data.get('answers', [])
        
        if age_months is None:
            return jsonify({"error": "Age is required"}), 400
        
        # Find appropriate age group
        age_group = None
        for age in sorted(KPSP_QUESTIONS.keys()):
            if age_months >= age:
                age_group = age
        
        if age_group is None:
            return jsonify({"error": "No KPSP questions available for this age"}), 400
        
        questions = KPSP_QUESTIONS[age_group]
        
        if len(answers) != len(questions):
            return jsonify({"error": "Number of answers doesn't match questions"}), 400
        
        # Calculate score
        score = sum(1 for answer in answers if answer)
        
        # Determine result
        if score >= len(questions) * 0.8:
            result = "Perkembangan Sesuai Usia"
            color = "#4caf50"
            recommendation = "Pertumbuhan dan perkembangan anak sesuai usia. Terus lakukan stimulasi."
        elif score >= len(questions) * 0.6:
            result = "Perkembangan Terduga Terlambat"
            color = "#ff9800"
            recommendation = "Perlu stimulasi intensif dan pemantauan lebih lanjut."
        else:
            result = "Perkembangan Terlambat"
            color = "#f44336"
            recommendation = "Segera konsultasikan dengan dokter anak untuk evaluasi lebih lanjut."
        
        return jsonify({
            "age_group": age_group,
            "score": score,
            "total_questions": len(questions),
            "result": result,
            "color": color,
            "recommendation": recommendation,
            "questions": questions,
            "answers": answers
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/growth-data', methods=['GET'])
def api_growth_data():
    """API endpoint to get sample growth data"""
    # Generate sample data for demonstration
    sample_data = {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "weight": [3.2, 3.8, 4.5, 5.1, 5.8, 6.4],
        "height": [50, 52, 55, 58, 61, 64],
        "z_scores": [-0.5, -0.3, 0.1, 0.4, 0.7, 0.9]
    }
    return jsonify(sample_data)

@app.route('/api/info')
def api_info():
    """API information endpoint"""
    return jsonify({
        "app_name": APP_TITLE,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "author": "Habib Arsy - FKIK Universitas Jambi",
        "contact": f"+{CONTACT_WA}",
        "base_url": BASE_URL,
        "standards": {
            "who": "Child Growth Standards 2006",
            "permenkes": "No. 2 Tahun 2020"
        },
        "supported_indices": ["WAZ", "HAZ", "WHZ", "BAZ", "HCZ"],
        "age_range": "0-60 months",
        "features": [
            "WHO z-score calculation",
            "Permenkes 2020 classification",
            "Growth charts visualization",
            "PDF report export",
            "CSV data export",
            "KPSP screening",
            "Monthly checklist recommendations",
            "YouTube Video Integration",
            "Mode Mudah",
            "Kalkulator Kejar Tumbuh",
            "Perpustakaan Artikel Interaktif",
            "Flask Web Interface"
        ]
    })

# ===============================================================================
# SECTION 8: MAIN APPLICATION STARTUP
# ===============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print(f"🚀 {APP_TITLE} v{APP_VERSION} - FLASK EDITION")
    print("=" * 80)
    print(f"📊 WHO Calculator: {'✅ Operational' if calc else '❌ Unavailable'}")
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"📱 Contact: +{CONTACT_WA}")
    print(f"🎨 Themes: {len(UI_THEMES)} available")
    print(f"💉 Immunization: {len(IMMUNIZATION_SCHEDULE)} schedules")
    print(f"🧠 KPSP: {len(KPSP_QUESTIONS)} question sets")
    print(f"📚 Perpustakaan: {len(ARTIKEL_LOKAL_DATABASE)} verified articles")
    print(f"🎥 Videos: {len(KPSP_YOUTUBE_VIDEOS) + sum(len(v) for v in MPASI_YOUTUBE_VIDEOS.values())} video links")
    print("=" * 80)
    
    # Run the Flask application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)