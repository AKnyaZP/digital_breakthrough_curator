from __future__ import annotations
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar

from aiogram.types import CallbackQuery, Message

from bot.analytics.amplitude import AmplitudeTelegramLogger
from bot.analytics.types import AbstractAnalyticsLogger, BaseEvent, EventProperties, EventType, UserProperties
from bot.core.config import settings
from bot.utils.singleton import SingletonMeta

T = TypeVar("T")


class AnalyticsService(metaclass=SingletonMeta):
    def __init__(self, logger: AbstractAnalyticsLogger) -> None:
        self.logger = logger

    async def _track_error(self, user_id: int, error_text: str) -> None:
        await self.logger.log_event(
            BaseEvent(
                user_id=user_id,
                event_type="Error",
                event_properties=EventProperties(text=error_text),
            ),
        )

    def track_event(self, event_name: EventType) -> Callable:
        """Decorator for tracking events in Amplitude, Google Analytics or Posthog."""

        def decorator(handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]]) -> Callable:
            @wraps(handler)
            async def wrapper(update: Message | CallbackQuery, *args: dict[str, T]) -> T | None:
                if (isinstance(update, (Message, CallbackQuery))) and update.from_user:
                    user_id = update.from_user.id
                    first_name = update.from_user.first_name
                    last_name = update.from_user.last_name
                    username = update.from_user.username
                    url = update.from_user.url
                    language = update.from_user.language_code
                else:
                    return None

                if isinstance(update, Message):
                    chat_id = update.chat.id
                    chat_type = update.chat.type
                    text = update.text
                    command = update.text if update.text and update.text.startswith("/") else None
                elif isinstance(update, CallbackQuery):
                    chat_id = update.message.chat.id if update.message else None
                    chat_type = update.message.chat.type if update.message else None
                    text = update.data
                    command = None

                await self.logger.log_event(
                    BaseEvent(
                        user_id=user_id,
                        event_type=event_name,
                        user_properties=UserProperties(
                            first_name=first_name,
                            last_name=last_name,
                            username=username,
                            url=url,
                        ),
                        event_properties=EventProperties(
                            chat_id=chat_id,
                            chat_type=chat_type,
                            text=text,
                            command=command,
                        ),
                        language=language,
                    ),
                )
                try:
                    result = await handler(update, *args)
                except Exception as e:
                    await self._track_error(user_id, str(e))
                    raise
                return result

            return wrapper

        return decorator


analytics = AnalyticsService(AmplitudeTelegramLogger(api_token=settings.AMPLITUDE_API_KEY))
