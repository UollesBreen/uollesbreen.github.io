import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

TOKEN = "8909172320:AAEi4syEF-95ndSwCSikFtnoiWGSi3JOHvY"
OWNER_ID = "5141107481"

bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Отправить пожелание",
                    callback_data="send_wish"
                )
            ]
        ]
    )


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Здесь вы можете отправить свою идею или пожалание, которое может быть реализовано партией Единый Лицей",
        reply_markup=get_keyboard()
    )


@dp.callback_query(F.data == "send_wish")
async def ask_wish(callback: CallbackQuery):
    await callback.message.answer(
        "Напиши своё пожелание следующим сообщением:"
    )
    await callback.answer()


@dp.message(F.text)
async def receive_wish(message: Message):
    if message.text.startswith("/"):
        return

    if message.from_user.id == OWNER_ID:
        return

    await bot.send_message(
        chat_id=OWNER_ID,
        text=(
            "📩 Новое пожелание!\n\n"
            f"{message.text}\n\n"
            f"ID отправителя: {message.from_user.id}"
        )
    )

    await message.answer(
        "Спасибо! Твоё пожелание отправлено!",
        reply_markup=get_keyboard()
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
