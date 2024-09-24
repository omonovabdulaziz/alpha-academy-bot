from dotenv import load_dotenv
import os
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB=os.getenv('POSTGRES_DB')
POSTGRES_HOST=os.getenv('POSTGRES_HOST')
POSTGRES_PORT=os.getenv('POSTGRES_PORT')
ADMIN_CHAT_ID=os.getenv('ADMIN_CHAT_ID')