import sys
import re
import logging
from sosmed_scanner.scanner import jalankan_pencarian

# Konfigurasi logging agar mencantumkan nama modul secara terstruktur
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

def main():
    if len(sys.argv) < 2:
        print("Cara penggunaan: python -m sosmed_scanner.cli [username]")
        sys.exit(1)
        
    target_username = sys.argv[1]
    
    # Validasi input menggunakan Regex (Hanya huruf, angka, underscore, titik, 1-30 karakter)
    if not re.match(r"^[A-Za-z0-9_.]{1,30}$", target_username):
        logger.error(f"Input tidak valid: '{target_username}'. Username hanya boleh berisi huruf, angka, titik, atau garis bawah.")
        sys.exit(1)
        
    jalankan_pencarian(target_username)

if __name__ == "__main__":
    main()
