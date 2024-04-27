from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from bot.keyboards.inline.contacts import contacts_keyboard
router = Router(name="info")

# "info", "help",

@router.message(Command(commands=["about"]))
async def about_handler(message: types.Message) -> None:
    """Information about bot."""
    await message.answer(_("about"), reply_markup=contacts_keyboard())


@router.message(Command(commands=["info"]))
async def info_handler(message: types.Message) -> None:
    """Information about bot."""
    await message.answer(_("first message"))
