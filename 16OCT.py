import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 1. SETUP HALAMAN ---
st.set_page_config(page_title="Pembelajaran Fisika", layout="wide")
st.title("Pembelajaran Fisika")

# --- 2. LOGIKA FISIKA (DARI FILE ASLI ANDA) ---
# Fungsi ini disalin langsung dari kode Pygame Anda karena logikanya universal
def snell(theta_inc, n1, n2):
    try:
        theta_i_rad = math.radians(theta_inc)
        # Menghindari error pembagian jika n2 = 0 (meski jarang terjadi di slider)
        if n2 == 0: return None 
        sin_theta_r = n1 * math.sin(theta_i_rad) / n2
        
        # Cek Total Internal Reflection
        if abs(sin_theta_r) > 1:
            return None
            
        theta_r_rad = math.asin(sin_theta_r)
        return math.degrees(theta_r_rad)
    except ValueError:
        return None

# --- 3. INPUT USER (PENGGANTI TOMBOL PYGAME) ---
# Di Streamlit, kita pakai Sidebar untuk kontrol, bukan tombol di layar
with st.sidebar:
    st.header("Pengaturan")
    
    # Pengganti tombol "Tambah/Kurang Sudut"
    angle_incident = st.slider("Sudut Datang (°)", 0, 89, 30)
    
    # Pengganti tombol "Tambah/Kurang Diameter"
    lens_diameter = st.slider("Diameter Lensa (px)", 60, 300, 120)
    
    # Pengganti tombol "Ganti Objek"
    object_type = st.selectbox("Pilih Objek", ["Panah", "Pensil", "Kaca", "Bola", "Buku"])
    
    # Pengaturan Indeks Bias (Tambahan agar lebih interaktif)
    n1 = st.number_input("n1 (Udara)", value=1.0, step=0.1)
    n2 = st.number_input("n2 (Lensa)", value=1.5, step=0.1)
    
    # Pengganti tombol Toggle
    show_reflection = st.checkbox("Tampilkan Refleksi", value=True)
    show_refraction = st.checkbox("Tampilkan Refraksi", value=True)

# --- 4. AREA GAMBAR (PENGGANTI PYGAME SCREEN) ---
# Kita menggunakan Matplotlib untuk menggambar grafik
fig, ax = plt.subplots(figsize=(10, 6))

# Set ukuran area gambar mirip dengan Pygame (1000x650)
WIDTH, HEIGHT = 1000, 650
ax.set_xlim(0, WIDTH)
ax.set_ylim(HEIGHT, 0) # Membalik sumbu Y agar (0,0) ada di kiri atas seperti Pygame
ax.set_aspect('equal')
ax.axis('off') # Hilangkan border grafik agar terlihat seperti kanvas

# Titik tengah
center_x, center_y = WIDTH // 2, HEIGHT // 2

# --- 5. FUNGSI GAMBAR ULANG ---

# A. Gambar Sumbu Optik
ax.axhline(y=center_y, color='black', linewidth=1)
ax.text(20, center_y - 20, "Sumbu Optik", fontsize=10)

# B. Gambar Lensa (Ellipse)
# Menggunakan Patches Matplotlib
lens = patches.Ellipse((center_x, center_y), 20, lens_diameter, 
                       edgecolor='none', facecolor='#96c8ff', alpha=0.6)
ax.add_patch(lens)
ax.text(center_x - 50, center_y + lens_diameter//2 + 20, "Lensa Cembung", fontsize=10)

# C. Gambar Objek
base_x = center_x - 300
base_y = center_y

if object_type == "Panah":
    ax.arrow(base_x, base_y, 0, -100, head_width=20, head_length=20, fc='blue', ec='blue', width=5)
elif object_type == "Bola":
    circle = patches.Circle((base_x, base_y - 50), 30, color='red')
    ax.add_patch(circle)
else:
    # Untuk penyederhanaan di Matplotlib, objek lain digambar sebagai kotak/garis
    rect = patches.Rectangle((base_x - 15, base_y - 100), 30, 100, color='brown')
    ax.add_patch(rect)
    ax.text(base_x - 20, base_y - 110, object_type, fontsize=12, color='blue')

# D. Gambar Sinar (Ray Tracing)
inc_len = 250
# Hitung koordinat awal sinar datang
inc_x = center_x - inc_len * math.cos(math.radians(angle_incident))
inc_y = center_y - inc_len * math.sin(math.radians(angle_incident))

# 1. Sinar Datang (Kuning)
ax.plot([inc_x, center_x], [inc_y, center_y], color='orange', linewidth=3, label='Sinar Datang')

# 2. Sinar Pantul (Merah)
if show_reflection:
    refl_x = center_x - inc_len * math.cos(math.radians(angle_incident))
    refl_y = center_y + inc_len * math.sin(math.radians(angle_incident))
    ax.plot([center_x, refl_x], [center_y, refl_y], color='red', linewidth=2, linestyle='--', label='Refleksi')

# 3. Sinar Bias (Hijau)
if show_refraction:
    refr_angle = snell(angle_incident, n1, n2)
    if refr_angle is not None:
        refr_len = 350
        refr_x = center_x + refr_len * math.cos(math.radians(refr_angle))
        refr_y = center_y + refr_len * math.sin(math.radians(refr_angle))
        ax.plot([center_x, refr_x], [center_y, refr_y], color='green', linewidth=3, label='Refraksi')
    else:
        ax.text(center_x + 50, center_y + 50, "TOTAL INTERNAL REFLECTION!", color='red', fontsize=12, fontweight='bold')

# --- 6. TAMPILKAN HASIL ---
# Menampilkan grafik matplotlib ke Streamlit
st.pyplot(fig)

# Info Box di bawah
st.info(f"""
**Info Simulasi:**
- Sudut Datang: {angle_incident}°
- Indeks Bias Medium 1: {n1}
- Indeks Bias Medium 2: {n2}
- Hasil Refraksi: {snell(angle_incident, n1, n2) if snell(angle_incident, n1, n2) else 'TIR'}°
""")



