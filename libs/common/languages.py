from enum import Enum


class Locale(Enum):
    en = "en-US"
    ru = "ru-RU"


langTgToLocale: dict = {
    "ru": Locale.ru,
    "en": Locale.en
}

_language_default_ = Locale.ru


def getTgLanguageLocale(lang: str) -> Locale:
    if lang in langTgToLocale:
        return langTgToLocale[lang]
    return _language_default_


def getLocaleByString(lang: str) -> Locale:
    if lang == Locale.en.value:
        return Locale.en

    return _language_default_
