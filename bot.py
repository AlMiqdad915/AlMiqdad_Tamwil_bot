import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# 📢 قنوات الاشتراك الإجباري الخاصة بك
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
            # إذا واجه البوت مشكلة في الفحص (مثلاً لم يُرفع كـ Admin بعد)، سيعتبره غير مشترك احتياطاً
            return False
    return True

# دالة إرسال القائمة الرئيسية بالأزرار المتكاملة (تطابق الصورة)
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback=False) -> None:
    # جلب بيانات المستخدم (افتراضية حالياً لغرض العرض كبداية)
    user = update.effective_user
    user_id = user.id
    points = 1421  # قيمة افتراضية تظهر للمشترك، يمكنك ربطها بقاعدة بيانات لاحقاً

    # نص الرسالة الترحيبية الاحترافية مطابقة للصورة
    welcome_text = (
        f"**- أهلاً بك في بوت تمويل الوزارة**\n"
        f"🆔 | **الآيدي حسابك** ⇐ {{ `{user_id}` }}\n"
        f"💰 | **نقاطك** ⇐ {{ `{points}` }} نقطة\n"
        f"📢 | تابع قناة التعليمات والشروحات الرسمية: [اضغط هنا للاشتراك](https://t.me/Abdullbari62287)\n\n"
        f"🚀 **البوت مخصص لتمويل وتصعيد قنوات ومجموعات التليجرام مجاناً وبأعلى سرعة.**"
    )

    # 📊 تصميم شبكة الأزرار تماماً كما في الصورة
    keyboard = [
        [InlineKeyboardButton(f"💎 رصيدك: {points}", callback_data="my_points")],
        [InlineKeyboardButton("📊 تمويل قناتك أو مجموعتك 📊", callback_data="promote_chat")],
        [InlineKeyboardButton("📋 المهام", callback_data="tasks"), InlineKeyboardButton("💎 تجميع النقاط", callback_data="collect_points")],
        [InlineKeyboardButton("↗️ شحن نقاط بالنجوم", callback_data="stars_charge"), InlineKeyboardButton("🔀 تحويل النقاط", callback_data="transfer_points")],
        [InlineKeyboardButton("🚬 معلومات حسابك", callback_data="account_info"), InlineKeyboardButton("📋 تمويلاتي", callback_data="my_promotions")],
        [InlineKeyboardButton("🤝 ادعُ صديقاً", callback_data="invite_friend"), InlineKeyboardButton("🎟 قسائمي", callback_data="coupons")],
        [InlineKeyboardButton("↗️ إكمال الطلبات", callback_data="order_status"), InlineKeyboardButton("⚡ اشترِ مضاعف النقاط", callback_data="buy_multiplier")],
        [InlineKeyboardButton("📢 قنواتنا الرسمية", callback_data="official_channels"), InlineKeyboardButton("🎁 استلم هديتك اليومية الآن 🎁", callback_data="daily_gift")],
        [InlineKeyboardButton("🎉 نجوم ⭐ جوائز 💸 ارقام 📱 رصيد 🎉", callback_data="prizes")],
        [InlineKeyboardButton("📥 شراء مشتركين حقيقيين ↗️", callback_data="buy_members")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if is_callback:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# دالة الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if await check_subscription(user_id, context):
        await send_main_menu(update, context, is_callback=False)
    else:
        # أزرار قنوات الاشتراك الإجباري
        buttons = []
        for channel in REQUIRED_CHANNELS:
            buttons.append([InlineKeyboardButton(f"📢 اشترك في {channel['username']}", url=channel['link'])])
        
        buttons.append([InlineKeyboardButton("🔄 تحقق من الاشتراك", callback_data="check_sub")])
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.reply_text(
            "⚠️ **عذراً يا عزيزي، يجب عليك الاشتراك في قنوات البوت أولاً لتتمكن من استخدامه والوصول إلى لوحة التحكم!**",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# دالة التعامل مع الأزرار التفاعلية (الردود عند الضغط على الأزرار)
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "check_sub":
        if await check_subscription(user_id, context):
            await send_main_menu(update, context, is_callback=True)
        else:
            buttons = []
            for channel in REQUIRED_CHANNELS:
                buttons.append([InlineKeyboardButton(f"📢 اشترك في {channel['username']}", url=channel['link'])])
            buttons.append([InlineKeyboardButton("🔄 تحقق من الاشتراك", callback_data="check_sub")])
            reply_markup = InlineKeyboardMarkup(buttons)
            
            try:
                await query.edit_message_text(
                    "❌ **لم تشترك في جميع القنوات بعد!** فضلاً اشترك في القنوات الثلاث ثم اضغط تحقق مجدداً لتظهر لك الأزرار الرئيسية.",
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            except Exception:
                pass
    
    # 💡 هنا يمكنك برمجة رد فعل مخصص لكل زر عند الضغط عليه مستقبلاً
    elif query.data == "collect_points":
        await query.message.reply_text("📥 قسم تجميع النقاط: قم بمشاركة رابط الدعوة الخاص بك لتجميع النقاط!")

# دالة التعامل مع الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not await check_subscription(user_id, context):
        await update.message.reply_text("⚠️ الرجاء الاشتراك في القنوات أولاً لتفعيل البوت ورؤية الأزرار! أرسل /start")
        return
    
    await update.message.reply_text("📬 أهلاً بك! استخدم الأزرار الظاهرة في القائمة الرئيسية للتحكم بالبوت والتمويل.")

def main() -> None:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ خطأ: لم يتم العثور على التوكين في السيرفر!")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("⚡ البوت يعمل الآن بلوحة الأزرار الكاملة بنجاح...")
    application.run_polling(close_loop=False)

if __name__ == '__main__':
    main()
