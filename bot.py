import os
import logging
from weather import get_weather_test
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = str(context.args[0])
    messages = await get_weather_test(city)
    for message in messages:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def launch_bot():
    TOKEN = os.getenv('BOT_TOKEN')
    LOCAL = bool(int(os.getenv('LOCAL')))
    WEBHOOK = os.getenv('WEBHOOK_URL')
    PORT = int(os.getenv('PORT'))
    IP = os.getenv('IP')
    
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('weather', weather))
    
    if LOCAL:
        print('polling messages...')
        application.run_polling()
    else:
        application.run_webhook()
        print(f'setting webhook on "{WEBHOOK}" listening on address "{IP}:{PORT}"...')
        application.run_webhook(
            listen=IP, 
            port=PORT, 
            url_path=TOKEN, 
            webhook_url=WEBHOOK)