import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# قنوات الاشتراك الإجباري (يمكنك تعديل المعرفات والروابط حسب قنواتك)
REQUIRED_CHANNELS = [
    {"username": "@test1", "link": "https://t.me/test1"},
    {"username": "@test2", "link": "https://t.me/test2"}
]

# دالة التحقق من الاشتراك الإجباري
async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel["username"], user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            return False
    return True

# دالة الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id

    if await check_subscription(user_id, context):
        # القائمة الرئيسية إذا كان مشتركاً
        keyboard = [
            [InlineKeyboardButton("💰 طلب تمويل", callback_type="request_finance")],
            [InlineKeyboardButton("📊 حسابي", callback_type="my_account"), InlineKeyboardButton("📞 الدعم الفني", callback_type="support")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"أهلاً بك يا {user.first_name} في بوت التمويل السريع! ✨\n\nالرجاء اختيار الخدمة المطلوبة من الأسفل:",
            reply_markup=reply_markup
        )
    else:
        # رسالة الاشتراك الإجباري إذا لم يكن مشتركاً
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
            await query.edit_message_text("❌ لم تشترك في جميع القنوات بعد! فضلاً اشترك واضغط تحقق مجدداً.")

# دالة التعامل مع الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not await check_subscription(user_id, context):
        await update.message.reply_text("⚠️ الرجاء الاشتراك في القنوات أولاً لتفعيل البوت! أرسل /start")
        return
    
    await update.message.reply_text("📥 تم استلام طلبك، سيقوم الدعم الفني بمراجعته والتواصل معك قريباً.")

def main() -> None:
    # 🔒 التعديل الحاسم لقراءة التوكين من إعدادات موقع Render بأمان وبدون حظر
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ خطأ: لم يتم العثور على التوكين في السيرفر!")
        return

    # بناء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة الحوافظ (Handlers)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # تشغيل البوت بشكل مستمر
    print("⚡ البوت يعمل الآن بنجاح وبأمان تام على السيرفر...")
    application.run_polling(close_loop=False)

if __name__ == '__main__':
    main()
