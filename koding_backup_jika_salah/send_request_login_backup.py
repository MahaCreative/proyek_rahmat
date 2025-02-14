import json
from datetime import datetime
import pytz
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
import asyncio
from termcolor import colored

tz = pytz.timezone("Asia/Jakarta")  # Ganti sesuai zona waktu yang diinginkan
now = datetime.now(tz)

class TelegramBot:
    def __init__(self, phone_number, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient(self.phone_number+now.strftime("_%d%m%y%H%M%S"), self.api_id, self.api_hash)
        self.phone_code_hash_map = {}

    async def send_request_code(self):
        await self.client.connect()
        try:
            print(f"Mengirim permintaan OTP ke {self.phone_number}...")
            result = await self.client.send_code_request(self.phone_number)
            self.phone_code_hash_map[self.phone_number] = result.phone_code_hash
            print(colored("Permintaan OTP berhasil dikirim.", "green"))
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

            print(f"Login dengan phone_code_hash: {phone_code_hash} dan OTP: {otp}")

            # ✅ Perbaiki urutan parameter
            await self.client.sign_in(self.phone_number, code=otp, phone_code_hash =phone_code_hash)

            me = await self.client.get_me()
            print(colored(f"Login berhasil! Nama Pengguna: {me.username}", "green"))
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
        except Exception as e:
            print(colored(f"Terjadi kesalahan saat login dengan password: {str(e)}", "red"))
        finally:
            await self.client.disconnect()

