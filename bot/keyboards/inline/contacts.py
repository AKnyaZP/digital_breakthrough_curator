from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.config import settings


def contacts_keyboard() -> InlineKeyboardMarkup:
    """Use when call contacts command."""
    buttons = [
        [InlineKeyboardButton(text=_("kgall739"), url="https://t.me/kgall739")],
        [InlineKeyboardButton(text=_("sabkvq"), url="https://t.me/sabkvq")],
        [InlineKeyboardButton(text=_("knyazev_artem"), url="https://t.me/knyazev_artem")],
        [InlineKeyboardButton(text=_("LanderWine"), url="https://t.me/LanderWine")],
        [InlineKeyboardButton(text=_("romanov9617"), url="https://t.me/romanov9617")],
        [InlineKeyboardButton(text=_("goglfoghart"), url="https://t.me/goglfoghart")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    return keyboard.as_markup()


def support_keyboard() -> InlineKeyboardMarkup:
    """Use when call support query."""
    buttons = [
        [InlineKeyboardButton(text=_("support button"), url=settings.SUPPORT_URL)],
        [InlineKeyboardButton(text=_("back button"), callback_data="title main keyboard")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    return keyboard.as_markup()
