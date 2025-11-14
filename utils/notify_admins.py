import logging
from datetime import datetime
from data.config import ADMINS


def on_startup_notify(dp):
    for admin in ADMINS:
        try:
            dp.bot.send_message(admin, "Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)


def send_admin_message(message: str, bot=None):
    """Admin xabar yuborish funksiyasi
    
    Args:
        message (str): Yuborilishi kerak bo'lgan xabar
        bot: Telegram bot instance (ixtiyoriy)
    """
    if bot is None:
        # Agar bot berilmagan bo'lsa, lazy import qilamiz
        from loader import bot as default_bot
        bot = default_bot
    
    formatted_message = f"[{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] {message}"
    
    for admin in ADMINS:
        try:
            bot.send_message(admin, formatted_message)
        except Exception as err:
            logging.exception(f"Admin {admin} ga xabar yuborishda xato: {err}")
