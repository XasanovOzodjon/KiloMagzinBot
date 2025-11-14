

#pip imports
from telegram.ext import ChatMemberHandler, MessageHandler, Filters, CommandHandler
from telegram import Update, ChatMember
from sqlalchemy.orm import Session

#local imports
from data.config import ADMINS
from models.users import User, Link, Group
from data.database import get_db
from utils.users_servise import get_user_by_telegram_id
from utils.notify_admins import send_admin_message


def left_member_hendler(update: Update, context):
    
    db = next(get_db())
    try:
        if update.message and update.message.left_chat_member:
            left_member = update.message.left_chat_member  # Obyektning o'zini olish
            chat = update.effective_chat
            new_group = db.query(Group).filter(Group.telegram_id == chat.id).first()
            
            if new_group is None:
                new_group = Group(
                    telegram_id=chat.id,
                    title=chat.title
                )
                db.add(new_group)
                db.commit()
                db.refresh(new_group)
                send_admin_message(f"[lefted.py] New group added: {chat.title} (ID: {chat.id})")
            
            left_user = get_user_by_telegram_id(db, left_member.id)
            if left_user is None:
                left_user = User(
                    telegram_id=left_member.id,
                    first_name=left_member.first_name,
                    last_name=left_member.last_name,
                    username=left_member.username,
                    group_id=None
                )
                db.add(left_user)
                db.commit()
                db.refresh(left_user)
                send_admin_message(f"[lefted.py] New user added: {left_member.full_name} (ID: {left_member.id})")
            else:
                left_user.group_id = None
                send_admin_message(f"[lefted.py] User left group: {left_member.full_name} (ID: {left_member.id}) from group {chat.title} (ID: {chat.id})")
                left_user_link = db.query(Link).filter(Link.new_user_id == left_user.id, Link.group_id == new_group.id).first()
                if left_user_link:
                    db.delete(left_user_link)
                    send_admin_message(f"[lefted.py] Link deleted for added user: {left_user_link.from_user_id}\n lefted user: {left_user_link.new_user_id}\nin group ID: {new_group.id}")
                    
                db.commit()
    except Exception as e:
        send_admin_message(f"[lefted.py] Error in left_member_handler: {e}")
        db.rollback()
    finally:
        db.close()
        
                    
def register_handlers(dp):
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, left_member_hendler))