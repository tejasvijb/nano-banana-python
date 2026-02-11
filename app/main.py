import os
from typing import Final
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

ACCESS_TOKEN: Final[str] = os.getenv("access_token")
BOT_USERNAME: Final[str] = os.getenv("bot_username")

# Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your friendly neighborhood bot. How can I assist you today?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I am a bannana! Please ask me anything you want to know about bananas or just say hi!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("This is a custom command response! You can customize this to do anything you want.")



#  Responses


def handle_response(text: str) -> str:
  processed: str = text.lower()

  if 'hello' in processed:
    return "Hello there! How can I assist you today?"
  
  if 'how are you' in processed:
    return "I'm just a bot, but I'm doing great! Thanks for asking."
  
  if 'i love bananas' in processed:
    return "Bananas are great! They're delicious and packed with nutrients."
  
  return "Sorry, I didn't understand that. Can you please rephrase?"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

  message_type: str = update.message.chat.type
  text: str = update.message.text

  print(f'User ({update.message.chat.id}) in {message_type} sent: {text}')

  if message_type == 'group':
    if BOT_USERNAME in text:
        new_text: str = text.replace(BOT_USERNAME, '').strip()
        response: str = handle_response(new_text)
    else:
        return
      
  else:
    response: str = handle_response(text)


  print(f'Bot response: {response}')
  await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
  print("Starting bot...")
  application = Application.builder().token(ACCESS_TOKEN).build()

  # Commands
  application.add_handler(CommandHandler('start', start_command))
  application.add_handler(CommandHandler('help', help_command))
  application.add_handler(CommandHandler('custom', custom_command))



  # Messasge handler
  application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

  # Error handler
  application.add_error_handler(error)

  # Polls the bot
  print("Bot is running...")
  application.run_polling(poll_interval=3)


