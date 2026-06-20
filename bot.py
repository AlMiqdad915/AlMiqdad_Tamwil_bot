import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# 📢 قنوات الاشتراك الإجباري التي أرسلتها
REQUIRED_CHANNELS = [
    {"username": "@Abdullbari62287", "link": "https://t.me/Abdullbari62287"},
    {"username": "@naseer_jobran", "link": "https://t.me/naseer_jobran"},
    {"username": "@Zawamil_Alkasir", "link": "https://t.me/Zawamil_Alkasir"}
]

# دالة التحقق من الاشتراك الإجباري
async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel["username"], user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            # في حال حدوث أي خطأ (مثلاً البوت ليس مشرفاً في القناة)، يفضل تركه يمر أو التحقق
            return False
    return True

# دالة الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id

    if await check_subscription(user_id, context):
        # القائمة الرئيسية بعد تحقق الاشتراك
        keyboard = [
            [InlineKeyboardButton("💰 طلب تمويل", callback_data="request_finance")],
            [InlineKeyboardButton("📊 حسابي", callback_data="my_account"), InlineKeyboardButton("📞 الدعم الفني", callback_data="support")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"أهلاً بك يا {user.first_name} في بوت التمويل السريع! ✨\n\nالرجاء اختيار الخدمة المطلوبة من الأسفل:",
            reply_markup=reply_markup
        )
    else:
        # رسالة الاشتراك الإجباري إذا لم يكن مشتركاً في القنوات الثلاث
        buttons = []
        for channel in REQUIRED_CHANNELS:
            buttons.append([InlineKeyboardButton(f"📢 اشترك في {channel['username']}", url=channel['link'])])
        
        buttons.append([InlineKeyboardButton("🔄 تحقق من الاشتراك", callback_data="check_sub")])
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.reply_text(
            "⚠️ عذراً يا عزيزي، يجب عليك الاشتراك في قنوات البوت أولاً لتتمكن من استخدامه!",
            reply_markup=reply_markup
        )

# دالة التعامل مع الأزرار التفاعلية
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "check_sub":
        if await check_subscription(user_id, context):
            await query.edit_message_text("✅ تم التحقق بنجاح! أرسل /start الآن لتظهر لك القائمة الرئيسية.")
        else:
            # إذا ضغط ولم يشترك بعد، تظهر له القنوات مرة أخرى
            buttons = []
            for channel in REQUIRED_CHANNELS:
                buttons.append([InlineKeyboardButton(f"📢 اشترك في {channel['username']}", url=channel['link'])])
            buttons.append([InlineKeyboardButton("🔄 تحقق من الاشتراك", callback_data="check_sub")])
            reply_markup = InlineKeyboardMarkup(buttons)
            
            await query.edit_message_text(
                "❌ لم تشترك في جميع القنوات بعد! فضلاً اشترك في القنوات الثلاث ثم اضغط تحقق مجدداً.",
                reply_markup=reply_markup
            )

# دالة التعامل مع الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not await check_subscription(user_id, context):
        await update.message.reply_text("⚠️ الرجاء الاشتراك في القنوات أولاً لتفعيل البوت! أرسل /start")
        return
    
    await update.message.reply_text("📥 تم استلام طلبك، سيقوم الدعم الفني بمراجعته والتواصل معك قريباً.")

def main() -> None:
    # قراءة التوكين من إعدادات Render
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ خطأ: لم يتم العثور على التوكين في السيرفر!")
        return

    # بناء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة الحوافظ
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # تشغيل البوت
    print("⚡ البوت يعمل الآن بنجاح وبأمان تام على السيرفر...")
    application.run_polling(close_loop=False)

if __name__ == '__main__':
    main()
