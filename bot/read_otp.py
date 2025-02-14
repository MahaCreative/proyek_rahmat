import asyncio
from telethon import TelegramClient, events
import re
# Ganti dengan API ID dan API Hash Anda dari my.telegram.org
API_ID = '22003089'
API_HASH = '2681d1c1b490e153681df7c0d6b20a3b'


async def main():
    # Inisialisasi Telethon Client
    session_name = input("Masukkan nomor yang ingin dibaca otpnya")

    client = TelegramClient(session_name, API_ID, API_HASH)
    await client.start()

    print("✅ Bot sedang berjalan...")

    # Event listener untuk semua pesan masuk6251
    @client.on(events.NewMessage)
    async def handler(event):
        sender = await event.get_sender()
        sender_name = sender.username or sender.first_name or "Tidak diketahui"
        chat_id = event.chat_id
        message_text = event.message.message

        print(f"\n📩 Pesan baru dari: {sender_name} (Chat ID: {chat_id})")
        print(f"📝 Isi Pesan: {message_text}")
        # Ekstrak kode dari pesan menggunakan regex
        match = re.search(r'Login code: (\d{5})', message_text)
        if match:
            login_code = match.group(1)
            print(f"🔑 Kode Login: {login_code}")
        else:
            print("⚠️ Tidak ada kode login yang ditemukan dalam pesan.")
    # Menjalankan bot secara terus-menerus
    await client.run_until_disconnected()

# Menjalankan program
asyncio.run(main())
