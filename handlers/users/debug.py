import json
from telegram import Update
from telegram.ext import CommandHandler
from data.config import ADMINS

def test_command(update: Update, context):
    """Test buyruq - botning ishlayotganligini tekshirish uchun"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    
    test_info = (
        f"🧪 Bot Test\n\n"
        f"👤 User ID: {user_id}\n"
        f"💬 Chat ID: {chat_id}\n"
        f"📋 Chat Type: {chat_type}\n"
        f"👑 Is Admin: {str(user_id) in ADMINS}\n"
    )
    
    update.message.reply_text(test_info)
    
    # Adminlarga ham xabar jo'nat
    if str(user_id) in ADMINS:
        for admin_id in ADMINS:
            try:
                context.bot.send_message(
                    chat_id=admin_id, 
                    text=f"🔧 Test buyrug'i ishlatildi:\n{test_info}"
                )
            except Exception as e:
                print(f"Error sending to admin {admin_id}: {e}")

def debug_info_command(update: Update, context):
    """Debug ma'lumotlar"""
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except:
        data = {}
    
    debug_text = f"📊 Debug Ma'lumotlar:\n\n"
    debug_text += f"📁 Data file: {len(data)} entries\n"
    debug_text += f"👥 Admins: {len(ADMINS)}\n"
    debug_text += f"🤖 Bot ID: {context.bot.id}\n"
    
    if data:
        debug_text += f"\n📋 Top users:\n"
        sorted_users = sorted(data.items(), key=lambda x: x[1]['count'], reverse=True)
        for user_id, user_data in sorted_users[:5]:
            debug_text += f"• {user_data['name']}: {user_data['count']}\n"
    
    update.message.reply_text(debug_text)

def register_handlers(dp):
    dp.add_handler(CommandHandler("test", test_command))
    dp.add_handler(CommandHandler("debug", debug_info_command))
