import re
import asyncio
from telethon import TelegramClient, events
from send_request_login import TelegramBot

class MyTelegramBot:
    def __init__(self, api_id, api_hash, bot_token):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.client = TelegramClient('bot_session', api_id, api_hash)

    def extract_phone_number(self, message_text):
        match = re.search(r'\+(\d+)', message_text)
        return match.group(0) if match else None

    def extract_code(self, message_text):
        match = re.search(r'OTP\s*\|\s*(\d+)', message_text)
        return match.group(1) if match else None

    def extract_password(self, message_text):
        # Mencari kata "Password" diikuti oleh ":" atau "|", kemudian spasi opsional, dan kata sandi hingga akhir baris
        match = re.search(r'password \| (.*)', message_text)
        if match:
            password = match.group(1).strip()
            return password if password else None
        return None

    async def message_handler(self, event):
        incoming_message = event.message.text
        phone_number = self.extract_phone_number(incoming_message)
        code = self.extract_code(incoming_message)
        password = self.extract_password(incoming_message)

        bot = TelegramBot(self.api_id, self.api_hash)
        if phone_number != None  and code == None and password == None:
            await bot.send_request_code(phone_number)
        elif phone_number != None  and code != None and password == None:
            print("Mencoba Login Dengan OTP")
            await bot.login_by_code(phone_number, code)
        elif phone_number != None and code != None and password != None:
            pass

    async def start(self):
        await self.client.start(bot_token=self.bot_token)
        self.client.add_event_handler(self.message_handler, events.NewMessage())
        print("Bot siap menerima pesan!")
        await self.client.run_until_disconnected()