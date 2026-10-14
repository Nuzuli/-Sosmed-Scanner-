import logging
import urllib.request
from urllib.error import HTTPError, URLError

def cek_platform(platform_name: str, url_template: str, username: str) -> bool:
    """Memeriksa apakah username terdaftar di platform tertentu via HTTP request."""
    url = url_template.format(username)
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                logging.info(f"[TERSEDIA] {username} ditemukan di {platform_name}")
                return True
    except HTTPError as e:
        if e.code == 404:
            logging.info(f"[TIDAK DITEMUKAN] {username} tidak ada di {platform_name}")
        else:
            logging.warning(f"[HTTP Error {e.code}] Kendala akses ke {platform_name}")
    except URLError as e:
        logging.error(f"[URL Error] Gagal terhubung ke {platform_name}: {e.reason}")
    except Exception as e:
        logging.error(f"[Unexpected Error] Masalah tidak terduga pada {platform_name}: {str(e)}")
    return False
