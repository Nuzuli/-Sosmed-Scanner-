"""
Sosmed-Scanner
Alat memeriksa keberadaan username di platform media sosial yang tersedia untuk umum.
Hanya memeriksa ketersediaan halaman profil publik — tidak mengakses data pribadi.
"""

import sys
import time
import urllib.request
from urllib.error import HTTPError, URLError

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
    "User-Agent": "Mozilla/5.0"
}

def cek_platform(nama_platform, pola_url, username):
    url = pola_url.format(username=username)
    try:
        permintaan = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(permintaan, timeout=10) as respon:
            if respon.status == 200:
                return f"✅  {nama_platform:15} → Ditemukan  : {url}"
            return f"❌  {nama_platform:15} → Tidak ditemukan"
    except HTTPError as e:
        if e.code == 404:
            return f"❌  {nama_platform:15} → Tidak ditemukan"
        return f"⚠️   {nama_platform:15} → Kode: {e.code}"
    except URLError:
        return f"⚠️   {nama_platform:15} → Tidak terhubung"
    except Exception:
        return f"❓  {nama_platform:15} → Error"

def jalankan_pencarian(username):
    print("=" * 60)
    print(f"🔍 Memeriksa username: '{username}'")
    print("Hanya memeriksa halaman profil publik.")
    print("=" * 60)
    print()
    
    ditemukan = 0
    tidak_ditemukan = 0
    
    for nama, url in PLATFORMS.items():
        hasil = cek_platform(nama, url, username)
        print(hasil)
        if "Ditemukan" in hasil:
            ditemukan += 1
        elif "Tidak ditemukan" in hasil:
            tidak_ditemukan += 1
        time.sleep(1)
    
    print()
    print("=" * 60)
    print(f"📊 Ditemukan: {ditemukan} | Tidak ditemukan: {tidak_ditemukan}")
    print("=" * 60)

if __name__ == "__main__":
    print("🌐 SOSMED-SCANNER")
    print()
    if len(sys.argv) < 2:
        username = input("Masukkan username: ").strip()
        if not username:
            print("❌ Tidak boleh kosong")
            sys.exit(1)
    else:
        username = sys.argv[1]
    jalankan_pencarian(username)
