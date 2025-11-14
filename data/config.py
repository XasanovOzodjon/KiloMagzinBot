from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
ADMINS = env.list("ADMINS")       # adminlar ro'yxati
IP = env.str("ip")                # Xosting ip manzili

DB_USER = env.str("DB_USER")          # Ma'lumotlar bazasi foydalanuvchisi
DB_PASSWORD = env.str("DB_PASSWORD")  # Ma'lumotlar bazasi paroli
DB_HOST = env.str("DB_HOST")          # Ma'lumotlar bazasi xosti
DB_PORT = env.int("DB_PORT")         # Ma'lumotlar bazasi porti
DB_NAME = env.str("DB_NAME")          # Ma'lumotlar bazasi nomi