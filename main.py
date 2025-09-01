import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import os

from users import register_user, is_authorized  # importa funções de controle

TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ---------- Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    register_user(user.id, user.username or user.first_name)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Irineu, você não sabe, nem eu !")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    register_user(user.id, user.username or user.first_name)

    novo_echo = f'Se você que disse : "{update.message.text}", não sabe... Imagine eu !'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=novo_echo)

# Função restrita
async def restrito(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    register_user(user.id, user.username or user.first_name)

    if not is_authorized(user.id):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="❌ Você não tem autorização para usar esta função.")
        return

    if not context.args:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Uso: /restrito <nome>")
        return

    nome = " ".join(context.args)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"✅ Função restrita executada com sucesso para o usuário: {nome}")

# ---------- Main ----------
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    application.add_handler(CommandHandler('restrito', restrito))

    application.run_polling()

