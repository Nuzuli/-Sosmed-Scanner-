import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Memuat variabel lingkungan dari file .env
load_dotenv()

class SocialMediaBot:
    def __init__(self):
        """Inisialisasi WebDriver Chrome secara otomatis dan aman."""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        # Opsional: Menonaktifkan deteksi otomatisasi dasar
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login_instagram(self):
        """Melakukan simulasi login ke platform Instagram dengan error handling."""
        username = os.getenv("IG_USERNAME")
        password = os.getenv("IG_PASSWORD")

        if not username or not password:
            print("[Error] Kredensial Instagram tidak ditemukan di file .env")
            return False

        try:
            print("[Info] Membuka halaman Instagram...")
            self.driver.get("https://instagram.com")
            
            # Menunggu elemen input muncul (Maksimal 15 detik)
            username_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_input = self.driver.find_element(By.NAME, "password")
            
            # Mengisi data login secara bersih
            username_input.clear()
            username_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
            
            print("[Sukses] Formulir login Instagram berhasil dikirim.")
            time.sleep(5)
            return True

        except TimeoutException:
            print("[Error] Elemen halaman Instagram tidak termuat tepat waktu.")
        except NoSuchElementException:
            print("[Error] Kolom input username atau password tidak ditemukan.")
        except Exception as e:
            print(f"[Error Terjadi Kesalahan]: {str(e)}")
        return False

    def login_tiktok(self):
        """Melakukan simulasi login ke platform TikTok dengan error handling."""
        username = os.getenv("TIKTOK_USERNAME")
        password = os.getenv("TIKTOK_PASSWORD")

        if not username or not password:
            print("[Error] Kredensial TikTok tidak ditemukan di file .env")
            return False

        try:
            print("[Info] Membuka halaman TikTok...")
            self.driver.get("https://tiktok.com")
            
            # Menunggu elemen input username/email muncul
            username_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @name='username']"))
            )
            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            
            # Mengisi data login
            username_input.clear()
            username_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
            
            print("[Sukses] Formulir login TikTok berhasil dikirim.")
            time.sleep(5)
            return True

        except TimeoutException:
            print("[Error] Elemen halaman TikTok tidak termuat tepat waktu.")
        except NoSuchElementException:
            print("[Error] Kolom input TikTok tidak ditemukan.")
        except Exception as e:
            print(f"[Error Terjadi Kesalahan]: {str(e)}")
        return False

    def close(self):
        """Menutup browser secara aman."""
        if self.driver:
            self.driver.quit()
            print("[Info] Browser berhasil ditutup secara aman.")

# Eksekusi Program Utama
if __name__ == "__main__":
    bot = SocialMediaBot()
    try:
        # Silakan aktifkan fungsi yang ingin diuji di bawah ini
        bot.login_instagram()
        # bot.login_tiktok()
        
        input("\nTekan Enter di terminal ini untuk menutup sesi...")
    finally:
        bot.close()
