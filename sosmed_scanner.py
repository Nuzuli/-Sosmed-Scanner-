"""
Sosmed-Scanner
Alat memeriksa keberadaan username di platform media sosial yang tersedia untuk umum.
Hanya memeriksa ketersediaan halaman profil publik — tidak mengakses data pribadi.
Penggunaan: python sosmed_scanner.py namapengguna
"""

import sys
import time
import urllib.request
from urllib.error import HTTPError, URLError

# Daftar platform yang akan diperiksa (hanya halaman profil publik)
PLATFORMS = {
    "GitHub": "https://github.com/{username}",
    "Twitter/X": "https://x.com/{username}",
    "Instagram": "https://www.instagram.com/{username}/",
    "TikTok": "https://www.tiktok.com/@{username}",
    "YouTube": "https://www.youtube.com/@{username}",
    "Reddit": "https://www.reddit.com/user/{username}",
    "LinkedIn": "https://www.linkedin.com/in/{username}",
    "Facebook": "https://www.facebook.com/{username}",
    "Telegram": "https://t.me/{username}",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def cek_platform(nama_platform, pola_url, username):
    """Cek apakah username terdaftar di platform tertentu (hanya cek halaman publik)"""
    url = pola_url.format(username=username)
    
    try:
        permintaan = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(permintaan, timeout=10) as respon:
            if respon.status == 200:
                return f"✅  {nama_platform:15} → Ditemukan  : {url}"
            else:
                return f"❌  {nama_platform:15} → Tidak ditemukan"
    except HTTPError as e:
        if e.code == 404:
            return f"❌  {nama_platform:15} → Tidak ditemukan"
        else:
            return f"⚠️   {nama_platform:15} → Tidak dapat diperiksa (kode: {e.code})"
    except URLError:
        return f"⚠️   {nama_platform:15} → Tidak dapat terhubung"
    except Exception as e:
        return f"❓  {nama_platform:15} → Kesalahan: {str(e)[:30]}"

def jalankan_pencarian(username):
    print("=" * 60)
    print(f"🔍 Memeriksa username: '{username}'")
    print("Hanya memeriksa halaman profil publik, tidak mengakses data pribadi.")
    print("=" * 60)
    print()
    
    hasil_ditemukan = 0
    hasil_tidak_ditemukan = 0
    
    for nama, url in PLATFORMS.items():
        hasil = cek_platform(nama, url, username)
        print(hasil)
        
        if "Ditemukan" in hasil:
            hasil_ditemukan += 1
        elif "Tidak ditemukan" in hasil:
            hasil_tidak_ditemukan += 1
        
        time.sleep(1)  # Jangan membebani server
    
    print()
    print("=" * 60)
    print(f"📊 Ringkasan: Ditemukan = {hasil_ditemukan} | Tidak ditemukan = {hasil_tidak_ditemukan}")
    print("⚠️  Catatan: Hasil perkiraan saja, verifikasi manual disarankan")
    print("=" * 60)

if __name__ == "__main__":
    print("🌐 SOSMED-SCANNER")
    print("Alat pengecek keberadaan username di media sosial (hanya info publik)")
    print()
    
    if len(sys.argv) < 2:
        username = input("Masukkan username yang ingin diperiksa: ").strip()
        if not username:
            print("❌ Username tidak boleh kosong")
            sys.exit(1)
    else:
        username = sys.argv[1]
    
    jalankan_pencarian(username)
