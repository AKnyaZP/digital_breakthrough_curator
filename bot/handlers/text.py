import pickle

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _
from catboost import CatBoostClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

from bot.keyboards.inline.contacts import contacts_keyboard

router = Router(name="text")


vectorizer = pickle.load(open('tgbot-rsv/model/vectorizer.pickle', 'rb'))
try:
    model = CatBoostClassifier()
    model.load_model('tgbot-rsv/model/catboost_cls')
except Exception:
    pass



@router.message()
async def text_handler(message: types.Message) -> None:
    """Return a button with a link to the project."""
    await message.answer("Подождите, пожалуйста, ИИ думает")
    try:
        vec = vectorizer.transform(['Как я могу?', 'Куда мне что?'])
        sent_labels = model.predict(vec)
        # prediction = ai_model.predict(message.text)
        # await message.answer(prediction.tolist())
        await message.answer(sent_labels)
    except Exception:
        await message.answer("Небольшие технические проблемы. Уже чиним")
    # await message.answer(message.text)
