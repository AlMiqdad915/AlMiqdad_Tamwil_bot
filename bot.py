import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# تفعيل نظام تسجيل الأخطاء (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# النص الترحيبي عند الضغط على /start
START_TEXT = (
    "👋 أهلاً بك في بوت المقداد للتمويل الذكي!\n\n"
    "🚀 بوابتك الأولى نحو تضخيم قناتك ومجموعتك بأعضاء حقيقيين، بسرعة واحترافية.\n\n"
    "✨ ماذا نقدم لك اليوم؟\n"
    "✔ زيادة فورية لأعضاء قناتك/مجموعتك.\n"
    "✔ نظام إحالات متقدم يضاعف أرباحك.\n"
    "✔ تقارير لحظية تمنحك تحكماً كاملاً.\n\n"
    "🔜 قريباً... خدمات حصرية إضافية (ترويج متقدم + سرفرات بوبجي) لعملائنا المميزين فقط!\n\n"
    "📌 كيف تبدأ؟\n"
    "اضغط على زر \"عرض الباقات\" لاختيار باقة التمويل المناسبة لك.\n\n"
    "بوت المقداد... حيث تتحول القنوات الصغيرة إلى منصات مؤثرة 📈 والطلبات إلى أوامر ⚡ بأعلى كفاءة ودقة متناهية."
)

# أسماء الأزرار
BUTTON_SERVICES = "🛒 الخدمات وتمويل قنواتك"
BUTTON_EARN = "💎 تجميع نقاط مجانية"
BUTTON_TRANSFER = "🔄 تحويل نقاط"
BUTTON_PACKAGES = "📦 عرض الباقات المدفوعة"
BUTTON_STATS = "📊 إحصائيات حسابي"
BUTTON_CHECK = "🔍 فحص ومتابعة الطلب"
BUTTON_SUPPORT = "📞 الدعم الفني والمراسلة"
BUTTON_EXCLUSIVE = "🎮 خدمات حصرية (قريباً)"

# هندسة وتوزيع الأزرار
MAIN_KEYBOARD = [
    [BUTTON_SERVICES],
    [BUTTON_EARN, BUTTON_TRANSFER],
    [BUTTON_PACKAGES, BUTTON_STATS],
    [BUTTON_CHECK, BUTTON_SUPPORT],
    [BUTTON_EXCLUSIVE]
]
reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

# دالة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(START_TEXT, reply_markup=reply_markup)

# دالة التعامل مع الأزرار
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    user = update.effective_user

    if user_text == BUTTON_SERVICES:
        await update.message.reply_text(
            "🛒 <b>قسم الخدمات والتمويل:</b>\n\n"
            "هنا يمكنك إطلاق حملات التمويل الخاصة بك وزيادة أعضاء قناتك أو مجموعتك فوراً.\n"
            "الرجاء تجميع النقاط أولاً أو شراء باقة مدفوعة للبدء.",
            parse_mode="HTML"
        )

    elif user_text == BUTTON_EARN:
        await update.message.reply_text(
            "💰 <b>قائمة كسب النقاط والأرباح مجاناً:</b>\n\n"
            "• 👥 <b>دعوة الأصدقاء (رابط الإحالة):</b> شارك رابطك واكسب نقاطاً عن كل مشترك جديد.\n"
            "• 📢 <b>الاشتراك في القنوات:</b> انضم للقنوات المدعومة واكسب نقاطاً فورية.\n"
            "• 🎁 <b>الهدية اليومية:</b> اضغط على الهدية مرة كل 24 ساعة للمطالبة بنقاط مجانية.",
            parse_mode="HTML"
        )

    elif user_text == BUTTON_TRANSFER:
        await update.message.reply_text(
            "🔄 <b>قسم تحويل النقاط:</b>\n\nيمكنك تحويل رصيد نقاطك إلى مستخدم آخر عن طريق إرسال الآيدي الخاص به وقيمة النقاط.",
            parse_mode="HTML"
        )

    elif user_text == BUTTON_STATS:
        stats_msg = (
            f"📊 <b>مستخدمنا العزيز، إليك تفاصيل حسابك الحالي:</b>\n\n"
            f"• 👤 <b>الاسم:</b> {user.first_name}\n"
            f"• 🆔 <b>الآيدي الخاص بك:</b> <code>{user.id}</code>\n"
            f"• 💰 <b>رصيد نقاطك:</b> <code>0 نقطة</code>\n"
            f"• 👥 <b>عدد إحالاتك:</b> <code>0 مستخدم</code>\n\n"
            f"🔗 <i>رابط الإحالة الخاص بك لكسب النقاط مجاناً:</i>\n"
            f"https://t.me/AlMiqdad_Tamwil_bot?start={user.id}"
        )
        await update.message.reply_text(stats_msg, parse_mode="HTML")

    elif user_text == BUTTON_PACKAGES:
        packages_msg = (
            "📦 <b>باقات تمويل وزيادة أعضاء تليجرام (أعضاء حقيقيين ومتفاعلين):</b>\n\n"
            "• 🌱 <b>الباقة البرونزية:</b> 500 عضو مقابل [أدخل السعر]\n"
            "• 🥈 <b>الباقة الفضية:</b> 1000 عضو مقابل [أدخل السعر]\n"
            "• 🥇 <b>الباقة الذهبية:</b> 5000 عضو مقابل [أدخل السعر]\n\n"
            "⚠️ <i>ملاحظة: لشراء أي باقة وتفعيلها فوراً، يرجى الضغط على زر الدعم الفني وتزويدنا برابط قناتك والباقة المطلوبة.</i>"
        )
        await update.message.reply_text(packages_msg, parse_mode="HTML")

    elif user_text == BUTTON_CHECK:
        await update.message.reply_text(
            "🔍 <b>قسم فحص ومتابعة الطلبات:</b>\n\nأدخل رقم طلب التمويل الخاص بك لمعرفة حالة التنفيذ اللحظية.",
            parse_mode="HTML"
        )

    elif user_text == BUTTON_SUPPORT:
        support_msg = (
            "📞 <b>قسم الدعم الفني والطلبات الخاصة:</b>\n\n"
            "نحن هنا لخدمتك ومساعدتك في تفعيل باقاتك أو حل أي مشكلة تواجهك. لتقديم طلب أو استفسار، تواصل مباشرة مع الإدارة عبر الحساب التالي:\n\n"
            "👤 <b>مطور البوت والدعم الفني:</b> @AlMiqdad_Support\n\n"
            "<i>أوقات الرد: متواجدون على مدار الساعة لخدمتكم بأفضل كفاءة!</i> ✨"
        )
        await update.message.reply_text(support_msg, parse_mode="HTML")

    elif user_text == BUTTON_EXCLUSIVE:
        await update.message.reply_text(
            "🎮 <b>خدمات حصرية (قريباً):</b>\n\nترقبوا إطلاق خدمات الترويج المتقدمة وسيرفرات شحن بوبجي لعملائنا المميزين قريباً جداً!",
            parse_mode="HTML"
        )

def main() -> None:
    # ضع هنا التوكين الخاص بالبوت الذي حصلت عليه من BotFather
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
