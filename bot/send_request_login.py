from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
import asyncio
from termcolor import colored


class TelegramBot:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient("session_name", self.api_id, self.api_hash)  # Gunakan sesi yang tetap
        self.phone_code_hash = None  # Simpan hash kode verifikasi

    async def send_request_code(self, nomor):
        await self.client.connect()
        try:
            print("Permintaan OTP sedang dikirim...")
            result = await self.client.send_code_request(nomor)
            self.phone_code_hash = result.phone_code_hash  # Simpan hash kode OTP
            print(colored("Permintaan OTP berhasil dikirim.", "green"))
        except Exception as e:
            print(colored(f"Terjadi kesalahan saat mengirim permintaan OTP: {e}", "red"))

    async def login_by_code(self, nomor, otp):
        if not self.phone_code_hash:
            print(colored("Error: phone_code_hash tidak ditemukan. Pastikan Anda telah mengirim OTP terlebih dahulu.",
                          "red"))
            return

        await self.client.connect()
        try:

            await self.client.sign_in(nomor, self.phone_code_hash, otp)
            me = await self.client.get_me()
            print(f"Nama Pengguna: {me.username}")
        except PhoneCodeInvalidError:
            print(colored("Kode OTP yang dimasukkan tidak valid. Pastikan Anda memasukkan kode yang benar.", "red"))
        except SessionPasswordNeededError:
            print("Akun memerlukan kata sandi untuk login. Silakan masukkan kata sandi.")
        except Exception as e:
            print(colored(f"Terjadi kesalahan: {str(e)}", "red"))
        finally:
            await self.client.disconnect()


# Contoh penggunaan
async def main():
    api_id = "22003089"  # Ganti dengan API ID Anda
    api_hash = "2681d1c1b490e153681df7c0d6b20a3b"  # Ganti dengan API Hash Anda
    nomor_telepon = "+62XXXXXXXXX"  # Ganti dengan nomor telepon Anda

    bot = TelegramBot(api_id, api_hash)
    await bot.send_request_code(nomor_telepon)

    otp = input("Masukkan kode OTP: ")  # Ambil OTP dari pengguna
    await bot.login_by_code(nomor_telepon, otp)


asyncio.run(main())
