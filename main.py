import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from vonage import Auth, Vonage
from vonage_messages import Sms

# የሎግ መረጃዎችን ለማየት
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# የቴሌግራም እና የቮኔጅ ቁልፎች (በRender Environment Variables ካስገባህ እነሱን ይጠቀማል)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8282990398:AAEsERZ3B9cs7hxz2pjstD4iuH521MfiXBg")
VONAGE_API_KEY = os.getenv("VONAGE_API_KEY", "8090e3cf")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET", "BVMD9qoiCSRxJPhs")

# የቮኔጅ ክላይንት ማስጀመሪያ
client = Vonage(
    Auth(
        api_key=VONAGE_API_KEY,
        api_secret=VONAGE_API_SECRET,
    )
)

# /start ትዕዛዝ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ሰላም! ኤስኤምኤስ ለመላክ በዚህ መልኩ ይጠቀሙ:\n"
        "/send <ስልክ_ቁጥር> <መልእክት>\n\n"
        "ምሳሌ: /send 251916067266 ሰላም እንዴት ነህ?"
    )

# /send ትዕዛዝ (ለማንኛውም ስልክ ቁጥር ኤስኤምኤስ መላኪያ)
async def send_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("ስህተት! እባክዎ ስልክ ቁጥር እና መልእክት ያስገቡ።\nምሳሌ: /send 251916067266 ሰላም")
        return

    phone_number = context.args[0]
    message_text = " ".join(context.args[1:])

    try:
        response = client.messages.send(
            Sms(
                to=phone_number,
                from_="Vonage APIs",
                text=message_text,
            )
        )
        await update.message.reply_text(f"✅ መልእክቱ ወደ {phone_number} ተልኳል!\nID: {response.message_uuid}")
    except Exception as e:
        await update.message.reply_text(f"❌ መልእክቱን መላክ አልተቻለም። ስህተት:\n{str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send", send_sms))
    
    print("ቦቱ እየሰራ ነው...")
    app.run_polling()
