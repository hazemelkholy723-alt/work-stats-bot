import os
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# --- سيرفر Flask عشان Replit ميفصلش ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- إعدادات البوت ---
TOKEN = "8558249602:AAG8Snts-MGowIJPFRiok9W3XD7DPujlWMQ"
ADMIN_ID = 8597163674
GROUP_ID = 0  # <--- هنغير ده لما البوت يقولنا الأيدي

users_db = {ADMIN_ID: {'name': 'حازم (الآدمن)', 'balance': 0, 'daily': 27}}
survey_temp = {}

QUESTIONS = [
    "1️⃣ الاسم الثلاثي؟", "2️⃣ رقم التليفون؟", "3️⃣ السن؟", "4️⃣ السكن؟",
    "5️⃣ المسمى الوظيفي؟", "6️⃣ سنوات الخبرة؟", "7️⃣ أهم مهاراتك؟", "8️⃣ هل اشتغلت في مكان مشابه؟",
    "9️⃣ المرتب الشهري؟", "🔟 سعر اليومية؟", "11️⃣ سعر الأوفر تايم؟", "12️⃣ حوافز أو بدلات؟",
    "13️⃣ مواعيد الشفت؟", "14️⃣ يوم الإجازة؟", "15️⃣ هدفك في الشغل؟"
]

def get_id(update, context):
    # أمر مخصص ليك عشان تعرف أيدي المجموعة
    update.message.reply_text(f"✅ أيدي هذه الدردشة هو:\n`{update.effective_chat.id}`", parse_mode='Markdown')

def start(update, context):
    user = update.effective_user
    if user.id in users_db:
        show_main_menu(update)
        return
    if context.args and context.args[0] == "join":
        update.message.reply_text("👋 أهلاً بك! سيتم بدء استطلاع الـ 15 سؤال لتفعيل حسابك.")
        survey_temp[user.id] = {'step': 0, 'answers': [], 'tg_name': user.full_name, 'tg_username': f"@{user.username}" if user.username else "لا يوجد", 'tg_id': user.id}
        update.message.reply_text(QUESTIONS[0])
        return
    update.message.reply_text(f"⚠️ الوصول محدود. تواصل مع: @hazem_elkholi")

def handle_message(update, context):
    user_id = update.effective_user.id
    if user_id in survey_temp:
        step = survey_temp[user_id]['step']
        survey_temp[user_id]['answers'].append(update.message.text)
        next_step = step + 1
        if next_step < len(QUESTIONS):
            survey_temp[user_id]['step'] = next_step
            update.message.reply_text(f"✅ ({next_step}/{len(QUESTIONS)})\n{QUESTIONS[next_step]}")
        else:
            data = survey_temp[user_id]
            answers = data['answers']
            try: daily_rate = float(answers[9])
            except: daily_rate = 0
            users_db[user_id] = {'name': answers[0], 'daily': daily_rate, 'balance': 0}
            
            report = (f"👤 **مشترك جديد**\n🆔 الأيدي: `{data['tg_id']}`\n🔗 اليوزر: {data['tg_username']}\n----------------\n")
            for i, q in enumerate(QUESTIONS): report += f"🔹 {q}: {answers[i]}\n"
            
            # إرسال للمجموعة (لو GROUP_ID تم ضبطه)
            if GROUP_ID != 0:
                context.bot.send_message(chat_id=GROUP_ID, text=report, parse_mode='Markdown')
            
            context.bot.send_message(chat_id=ADMIN_ID, text="✅ تم تسجيل مشترك جديد (التقرير في المجموعة).")
            update.message.reply_text("🎊 تم تفعيل حسابك بنجاح!")
            del survey_temp[user_id]
            show_main_menu(update)

def show_main_menu(update):
    user_id = update.effective_user.id
    user_data = users_db[user_id]
    keyboard = [[InlineKeyboardButton(f"➕ تسجيل يومية ({user_data['daily']}ج)", callback_data='add')],
                [InlineKeyboardButton("💰 رصيدي", callback_data='balance')]]
    text = f"مرحباً بك: {user_data['name']}\nنظام المحاسبة الخاص بك جاهز."
    if update.message: update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else: update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

def button_click(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()
    if query.data == 'add':
        users_db[user_id]['balance'] += users_db[user_id]['daily']
        query.edit_message_text(f"✅ تم إضافة يومية. رصيدك الحالي: {users_db[user_id]['balance']} ج", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data='main')]]))
    elif query.data == 'main': show_main_menu(update)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("get_id", get_id))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button_click))
    
    keep_alive()
    print("Bot is starting...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__': main()
