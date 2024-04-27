from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from bot.keyboards.inline.contacts import contacts_keyboard

router = Router(name="text")


@router.message()
async def text_handler(message: types.Message) -> None:
    """Return a button with a link to the project."""
    await message.answer(message.text)
