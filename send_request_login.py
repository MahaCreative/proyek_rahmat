from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
import asyncio


class TelegramBot:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient('session_name', api_id, api_hash)

    async def login(self, nomor, otp=None):
        await self.client.connect()
        try:
            if not await self.client.is_user_authorized():
                # Jika user belum login, kirim kode OTP

                await self.client.send_code_request(nomor)
                print("Permintaan OTP Berhasil Di Kirim")
                # Minta OTP jika belum diberikan
                if otp:

                    await self.client.sign_in(nomor, otp)
                    me = await self.client.get_me()
                    print(f"Nama Pengguna: {me.username}")
            else:
                print("Login telah berhasil")
                # Mendapatkan informasi pengguna setelah login berhasil
                me = await self.client.get_me()
                print(f"Nama Pengguna: {me.username}")
        except PhoneCodeInvalidError:
            # Jika kode OTP salah
            print("Kode OTP yang dimasukkan salah. Silakan coba lagi.")
        except SessionPasswordNeededError:
            # Jika otentikasi dua faktor diperlukan (password)
            print("Akun memerlukan kata sandi untuk login. Silakan masukkan kata sandi.")
        except Exception as e:
            # Menangani kesalahan umum lainnya
            print(f"Terjadi kesalahan: {str(e)}")
        finally:
            # Pastikan untuk menutup koneksi
            await self.client.disconnect()

