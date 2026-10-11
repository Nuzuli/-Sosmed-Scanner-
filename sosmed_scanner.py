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

def scan_username(username):
    print(f"\n🔍 Memulai pemindaian untuk username: {username}")
    print("-" * 50)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username=username)
        req = urllib.request.Request(url, headers=headers)
        
        try:
            # Beri jeda antar request agar aman dari rate-limit
            time.sleep(1) 
            
                    
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    print(f"✅ [DITEMUKAN] {platform}: {url}")
                    
        except HTTPError as e:
            if e.code == 404:
                print(f"❌ [TIDAK ADA] {platform}")
            else:
                print(f"⚠️ [ERROR {e.code}] {platform}")
        except URLError:
            print(f"📡 [KONEKSI GAGAL] {platform}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_user = sys.argv[1]
    else:
        target_user = input("Masukkan username yang ingin dicari: ").strip()
        
    if target_user:
        scan_username(target_user)
    else:
        print("Username tidak boleh kosong!")


