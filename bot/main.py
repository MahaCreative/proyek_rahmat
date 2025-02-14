from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from read_message import MyTelegramBot
from unittest.mock import patch
# Ganti dengan api_id dan api_hash yang kamu dapatkan dari my.telegram.org
api_id = '22003089'
api_hash = '2681d1c1b490e153681df7c0d6b20a3b'

# Nomor telepon yang digunakan untuk login

print("WELCOME HACKERES, PLEASE LOGIN YOU ARE TELEGRAM ACCOUNT IF YOU WANT TO USE THIS APP")
phone_number = input("Please Insert Phone Number :")
# Membuat instance client
client = TelegramClient('my_account_session', api_id, api_hash)
both = MyTelegramBot(api_id, api_hash, bot_token=None)
async def main():
    await client.connect()
    try:
        if not await client.is_user_authorized():

            await client.start(phone_number)

            # Mendapatkan informasi pengguna setelah login berhasil
            me = await client.get_me()
            print(f"Nama Pengguna: {me.username}")

        else:
            print("Login telah berhasil")
            await both.start()
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
        await client.disconnect()

# Menjalankan program
import asyncio
# with patch('builtins.input', side_effect=mock_input):
asyncio.run(main())