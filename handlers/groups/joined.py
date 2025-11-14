#standard imports

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


def new_member_hendler(update: Update, context):
    
    db = next(get_db())
    try:
        if update.message and update.message.new_chat_members:
            user_from = update.message.from_user
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
                send_admin_message(f"[joined.py] New group added: {chat.title} (ID: {chat.id})")
            
            for new_member in update.message.new_chat_members:
                user_from_db = get_user_by_telegram_id(db, user_from.id)
                
                # Yangi a'zoni tekshirish va yaratish
                existing_new_user = get_user_by_telegram_id(db, new_member.id)
                if existing_new_user is None:
                    new_user = User(
                        telegram_id=new_member.id,
                        first_name=new_member.first_name,
                        last_name=new_member.last_name,
                        username=new_member.username,
                        group_id=new_group.id
                    )
                    db.add(new_user)
                    db.commit()
                    db.refresh(new_user)
                    send_admin_message(f"[joined.py] New user added: {new_member.full_name} (ID: {new_member.id})\n to group {chat.title} (ID: {chat.id})")
                else:
                    new_user = existing_new_user
                    new_user.group_id = new_group.id
                    send_admin_message(f"[joined.py] Existing user joined: {new_member.full_name} (ID: {new_member.id})\n to group {chat.title} (ID: {chat.id})")
                    db.commit()
                
                if new_member.id != user_from.id:
                    # Boshqa foydalanuvchi tomonidan qo'shilgan
                    if user_from_db is None:
                        user_from_db = User(
                            telegram_id=user_from.id,
                            first_name=user_from.first_name,
                            last_name=user_from.last_name,
                            username=user_from.username,
                            group_id=new_group.id
                        )
                        db.add(user_from_db)
                        db.commit()
                        db.refresh(user_from_db)
                        send_admin_message(f"[joined.py] New user added: {user_from.full_name} (ID: {user_from.id})\n to group {chat.title} (ID: {chat.id})")
                    
                    # Takrorlangan link yaratmaslik uchun tekshirish
                    existing_link = db.query(Link).filter(
                        Link.from_user_id == user_from_db.id,
                        Link.new_user_id == new_user.id,
                        Link.group_id == new_group.id
                    ).first()
                    
                    if not existing_link:
                        new_link = Link(
                            from_user_id=user_from_db.id,
                            new_user_id=new_user.id,
                            group_id=new_group.id
                        )
                        db.add(new_link)
                        db.commit()
                        send_admin_message(f"[joined.py] {user_from_db.first_name} added {new_user.first_name} in group ID {new_group.id}")
                else:
                    # O'zi kirgan
                    if user_from_db is None:
                        user_from_db = User(
                            telegram_id=user_from.id,
                            first_name=user_from.first_name,
                            last_name=user_from.last_name,
                            username=user_from.username,
                            group_id=new_group.id
                        )
                        db.add(user_from_db)
                        db.commit()
                        db.refresh(user_from_db)
                        send_admin_message(f"[joined.py] New user added: {user_from.full_name} (ID: {user_from.id})\n to group {chat.title} (ID: {chat.id})")
                    else:
                        user_from_db.group_id = new_group.id
                        db.commit()
                        send_admin_message(f"[joined.py] Existing user joined: {user_from.full_name} (ID: {user_from.id})\n to group {chat.title} (ID: {chat.id})")
                    
                    # Takrorlangan link yaratmaslik uchun tekshirish
                    existing_self_link = db.query(Link).filter(
                        Link.from_user_id == None,
                        Link.new_user_id == new_user.id,
                        Link.group_id == new_group.id
                    ).first()
                    
                    if not existing_self_link:
                        new_link = Link(
                            from_user_id=None,
                            new_user_id=new_user.id,
                            group_id=new_group.id
                        )
                        db.add(new_link)
                        db.commit()
    except Exception as e:
        send_admin_message(f"[joined.py] Error in new_member_handler: {e}")
        db.rollback()
    finally:
        db.close()
                
                    

                
def register_handlers(dp):
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member_hendler))