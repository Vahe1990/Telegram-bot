import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import asyncio

API_TOKEN = '7886310382:AAEuAxcLpXdkfcCsTYwcCI9oWu4DsH-qosI'
CHANNEL_USERNAME = '@sofinolog'  # канал, где нужно быть подписанным

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("✅ Перейти к каналу", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"),
        InlineKeyboardButton("🔄 Проверить подписку", callback_data='check_sub')
    )
    await message.answer("👋 Привет! Подпишись на канал и нажми 'Проверить подписку'", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'check_sub')
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            await bot.answer_callback_query(callback_query.id, "✅ Вы подписаны!")
            await bot.send_message(user_id, "🎉 Отлично! Перейди к следующему шагу 👉 @SofWB_bot")
        else:
            raise Exception("Not subscribed")
    except:
        await bot.answer_callback_query(callback_query.id, "❌ Вы не подписаны. Подпишитесь и попробуйте снова.", show_alert=True)

# Запуск
if __name__ == '__main__':
    async def main():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling()
    asyncio.run(main())