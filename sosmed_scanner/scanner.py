import logging
from sosmed_scanner.network import cek_platform

def jalankan_pencarian(username: str):
    """Menjalankan pemindaian username di platform target."""
    if not username or not isinstance(username, str):
        logging.error("Input tidak valid. Username harus berupa teks.")
        return

    platforms = {
        "GitHub": "https://github.com{}",
        "Instagram": "https://instagram.com{}/",
        "TikTok": "https://tiktok.com@{}"
    }

    logging.info(f"Memulai pemindaian untuk username: {username}")
    for platform, url in platforms.items():
        cek_platform(platform, url, username)
