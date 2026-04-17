import os
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- إعداداتك ---
TOKEN = "8558249602:AAG8Snts-MGowIJPFRiok9W3XD7DPujlWMQ"
ADMIN_ID = 8597163674
GROUP_ID = 0 # سيبه صفر دلوقتي لحد ما تجيب الرقم

def get_group_id(update, context):
    # أمر مخصص عشان يظهرلك أيدي المجموعة
    chat_id = update.effective_chat.id
    update.message.reply_text(f"✅ أيدي هذه الدردشة هو:\n`{chat_id}`", parse_mode='Markdown')

def start(update, context):
    # كود البداية والأسئلة (اللي عملناه قبل كدة)
    update.message.reply_text("البوت شغال! لو أنت في المجموعة ابعت /get_id")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("get_id", get_group_id))
    dp.add_handler(CommandHandler("start", start))
    
    keep_alive()
    updater.start_polling()
    updater.idle()

if __name__ == '__main__': main()
