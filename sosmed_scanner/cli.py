import sys
import logging
from sosmed_scanner.scanner import jalankan_pencarian

# Konfigurasi logging dasar ke stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def main():
    if len(sys.argv) < 2:
        print("Cara penggunaan: python -m sosmed_scanner.cli [username]")
        sys.exit(1)

    target_username = sys.argv[1]
    jalankan_pencarian(target_username)

if __name__ == "__main__":
    main()
