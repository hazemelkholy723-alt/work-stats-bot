import os
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# --- إعداد السيرفر لضمان عدم التوقف ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- الحسابات: شفت بـ 27، إجازة بـ 54 ---
SHIFT_PRICE = 27
VACATION_DEDUCTION = 54

def start(update, context):
    keyboard = [[InlineKeyboardButton("تسجيل شفت (27ج)", callback_data='shift')],
                [InlineKeyboardButton("تسجيل إجازة (-54ج)", callback_data='vacation')]]
    update.message.reply_text('يا حازم، سجل عملياتك:', reply_markup=InlineKeyboardMarkup(keyboard))

def button(update, context):
    query = update.callback_query
    query.answer()
    res = f"✅ تم زيادة {SHIFT_PRICE}ج" if query.data == 'shift' else f"❌ تم خصم {VACATION_DEDUCTION}ج"
    query.edit_message_text(text=res)

def main():
    # ضع التوكن الخاص بك هنا بين العلامتين ""
    TOKEN = "حط_التوكن_بتاعك_هنا"
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    keep_alive()
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
