from . import en
from . import ru

_locales = {}
_currentLocale: str = "en"


def loc(ids):
    return _locales.get(_currentLocale, {}).get(ids, ids)


def use_locale(locale: str):
    global _currentLocale
    _currentLocale = locale


def update_locale(locale: str, data: dict):
    _locales.setdefault(locale, {}).update(data)


update_locale(ru.LOCALE, ru.DATA)
update_locale(en.LOCALE, en.DATA)

use_locale(ru.LOCALE)
