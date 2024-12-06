import requests
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7625684107:AAGPgXN0vcln5eq_CELeWNvPkCZ0y9GX_pM"

# تابع دریافت قیمت ارزهای دیجیتال از CoinGecko
def get_crypto_price(crypto_id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": crypto_id, "vs_currencies": "usd"}
        response = requests.get(url, params=params)
        response.raise_for_status()  # بررسی خطاهای HTTP
        data = response.json()
        return data[crypto_id]["usd"]  # قیمت در واحد دلار آمریکا
    except Exception as e:
        return f"خطا در دریافت قیمت {crypto_id}: {e}"

# دستورات استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ایجاد کیبورد سفارشی
    keyboard = [
        ["قیمت بیت کوین (BTC)", "قیمت اتریوم (ETH)"],  # دکمه‌ها
        ["قیمت ریپل (XRP)", "قیمت کاردانو (ADA)"],
        ["قیمت بایننس‌کوین (BNB)", "قیمت سولانا (SOL)"],
        ["قیمت ترون (TRX)"],
        ["اطلاعات بیشتر", "راهنما"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)  # کیبورد برای کاربر ارسال شود
    await update.message.reply_text(
        "به ربات ارزهای دیجیتال خوش آمدید!\nاز گزینه‌های زیر یکی را انتخاب کنید:",
        reply_markup=reply_markup
    )

# پاسخ به انتخاب کاربر
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text  # پیام کاربر
    
    # مدیریت دکمه‌ها
    crypto_map = {
        "قیمت بیت کوین (BTC)": "bitcoin",
        "قیمت اتریوم (ETH)": "ethereum",
        "قیمت ریپل (XRP)": "ripple",
        "قیمت کاردانو (ADA)": "cardano",
        "قیمت ترون (TRX)": "tron",
        "قیمت بایننس‌کوین (BNB)": "binancecoin",
        "قیمت سولانا (SOL)": "solana"
    }

    # بررسی و نمایش قیمت
    if user_message in crypto_map:
        crypto_id = crypto_map[user_message]
        price = get_crypto_price(crypto_id)
        await update.message.reply_text(f"{user_message}: {price} دلار")
    elif user_message == "اطلاعات بیشتر":
        await update.message.reply_text("این ربات برای ارائه اطلاعات قیمت ارزهای دیجیتال طراحی شده است.")
    elif user_message == "راهنما":
        await update.message.reply_text("برای شروع، یکی از گزینه‌ها را انتخاب کنید.")
    else:
        await update.message.reply_text("گزینه نامعتبر است. لطفاً یکی از گزینه‌های کیبورد را انتخاب کنید.")

# اجرای ربات
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    
    # افزودن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # شروع polling
    application.run_polling()
