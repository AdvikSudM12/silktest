#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль с встроенными иконками для использования в приложении.
Иконки закодированы в base64, чтобы не зависеть от внешних файлов.
"""

from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QByteArray, QBuffer, QIODevice
import base64

# Иконка Excel файла (фиолетовый документ)
EXCEL_ICON = """
iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAE+0lE
QVRogdWaXWgcVRTHf2d2drNpP2zTbGqa0jZ+JPWjrR+tVWyRilYFHwShSnyRgpSCPohPRaggvhR8EcSK
FfFFRDGiKFLxo9ZqW2sVrVptrSbU2KSbbLLZndnx4c5ms8lmZ2czG8H/y517z9z/Oeeee+65dyKqSlOC
QA3PBGrCZK8nLlMcxMaULPYt4UQpKRYVwCJU+xnw0ZwmS+F30AHUjxMkuKKYBGGxe0WGBzYSbQZMg01k
2I/jrcCxfBLzChAYagUDVFHpJbSWAzlSNKAB0AbiiHQA04AWY0CgBFNQiYHpItrJqPWZX/VHiJ2jnUBF
XSC4uZOJTg8v1tS8T1rHoDpE7JsLiKCaHVjA5sBWZhIkpjP3vPtqgLuDxVwS8G9exUxfDzZWe3PFSLqP
NmNM0ePzBChPgDsagxIAYMDYoXyj8gtQ+QnxHZQhADXmbT8xfgEyUEKE/J1S7wy4uMM5Y+2KLtZd6+Pk
6S9Y3riGCHHGeCPrhBMAA2L9v8e4VwDQOHeuK8ZnRLiFY2d6cB0Lm97sMdktQQNQ6+bLKUKCYbKKRImr
JTbf8+iJGMYmM6FH/PJL4G4LH4C4f5OzjKcHGXl2GwCr7roPCe5kX+9WbKJMdF0OkYulhWgLCPnwNu4x
TjLy3OPUN92MYiDlUV3bjrXnUTp/+ISLGl7BpIqUfA0GsAFsgc1YhiKw7r4nSaRGSUxfYnLkN2ZGf6e6
8UaUapJLQ8xPxJjrLRZIiYhQ7ckOBzp5ovNDOr/7kJWrb6Oi4jzTI5089OxuvFQCZeVSaLHdXASCEsoG
z3sWJ3I/gDZ2sJ0nO3cxfaGHoWNfsHzFGoLBJNGpOMnFNcDaYuNLQcmtFEYHqdr4J8nJ49THPqS69k/G
Rv7AwyJdBkTwlFHpz3J5v4hwVm5i6tq32dr2LF7aQl2XdNrLxNQu7hxL5Rwz7dJYKFm8VN7+5Jrn6e59
mVjfz6CgAiJadiIpXwAlTcVVTTS13MF47Bfia25jz8HDdB49wcj4yfLTyoEvAZRqqppu4vzAEeLDZ7C9
JP2ne7jl1rvoP/EjF0cGypLY/HJQhkXW2HgbN9z8ED/t3MXAqQN4nosCZ/q7cZNLBLbfWQ4KWQIyC6Wi
Zi1V9ZsY7h/BpqymXFOlWzIJLUAhS8BQgVJHbf0GqmobOXNsmNTiXLlUQPMMWuDMNRMi5zE4ICuoW9bA
QWVZ/EeWVS+HtJ1LhgIsMOX6VQmw6cEnqFtxM8c+3+ErDtjcMbkEVBBnOYpLVaQBJ1BFz48HcFN2GWct
UJWv/0Ln4jIKaCWKYlGCzlpCkRqO7d/JzEQ5kbTAjvhBIBcWIb0ck6rGS6RwXXdh2/IxP58iFCoFk4Q4
JzQKAUJVEV8Z3EMLS42l0TJ0vALYBBlxT/uKU2CJJGAhjJG0jvuJ8wtgcIiyRDKLIPw9cY6YfxRQiVun
EQmAFPmtKoIzNI2TWZTwXDeLXwIQQ3QQ5FLWIlbyMcgwIoPgZHczzvXnluRfBXs4EH2HuZXpJUfj9OZO
fhW9lMzupXA/HQb4KP42o+4ARpQAkA4k+d1u57VIhqk1fV6RdYkRRZkCPLxMSHNH1j9mZ9GpXRqKfCMJ
o3YDk+5ZYqZv7pQWQb1alKoCRfF3lLLgf5Wo/P97/LvgH5Jm8Xcw+pnLAAAAAElFTkSuQmCC
"""

# Иконка папки (фиолетовая папка)
FOLDER_ICON = """
iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAErklE
QVRoge2ZW2xURRjHf9/Zc7bbC9ttoaWUQm2xiJRyqRARDQpeojHRB/XNmKA+mJj4YDTGxEQfJCbGB30x
MZIYjYkm3iTEEjWNClWuIkUo0KaFlkK77e7Zc8Zvj8RW9tJeC9JNyD+Z7OzMfOf7zeXMmRlRVe5lmMuc
3AGghZS5TCPVgRmtjX0k5Xfg2RwAliC6CTijKqfSJtYMDPQU+tg2S9aVbJQagSRRfRcjT1aMnQzH/QdA
M6DPVA5njx1mHnAvLrAD9OeKsesBqnA3mAQ8CeRwgfcsgD07i0YWnB4GAHIegOdX7uYGwVv3I3RV9A/V
NwG0X2Q7UD82ZMcC1Ddj9x0AiB46RmLBL4gyUTcnTsM2cTb3w6MXkMdH2JkswGYa+nRkJKf73kW0F/dU
L2JjQONtPDsP0UXF8jSZu0FH3qHIV+Cc7EHsAB5tgERkzAxwpQDzAc7BHtxvh4mYfpxf/wYvlWvXFRWL
U6gUW4BfuCKBjcAJgEuDGRLHBnG2rkS6WpDOlqxjZxPFDJM8c3rkRiqxhHgT8YFM9Jd+3M8vYI6cw+69
WKpvzWbZHYhOEJu8F/gICPqJBFZOcOCd4nLyp/X43w8TfXGE1L5TeM8sRJobc/mmCcUCR4EtQBrVJbW2
oBSB8y1CwbZu3J3duLuPkXpjgNTrR0jvOYYsbi7ZtzagLAOOlpWbwMRADYvrgdU3kdg6wPmhE6S3H8Z0
txaVVwvoPKC2rFwJKIhKrAVYoVIlARkRXnPzMk42duP9MAyNNWAtU9Y04XW34G9bjXNgmMQrx0jvOoFp
nbp0olOBVMWr2hKRYlW0TKnSJnPyGQZ/S7H44cfxXliPCZjpnXc1Yt9YTvC9NQQ/3EDgw7UEP9tE4P0u
AltbMJHk9PcUQcVeYDKvz6KIdzjChPsGSL91HPfLIUww/T87O56m2IcWYB9agFnbTuLZAdz3j2LODkzr
/dMVmOoNlEOuYgCz1+FaH68RpzFOdCjG2I5fSL/9C96+IeRCIntsWiMyN0rsqf3Edw1iO5vK9h8HgMsi
KhUiOXp89/9VaPriuPuHSH74Pd7eQWT4IuIPDNJQcZk9LyJpMCmIxCFWOxeKJsZAMYZxCTFYE8SNK+KV
Hl9XAGF2FIoG0bHuGSdTbUiDLHvXtQtZfI8LsKEQMvAD9D4DZj5s/hLCbZnroQjQCfQTaYL5r8LSOzMb
uZqgduOVDQFU9deoRLEv1x9Hjj8P878BjMw9/gwv3ZGpLqODmeGhP+HXR2Dvemj7HUK1H76gR7UxVo+W
mVY1rdTR0c+hqx9aBkxRjwAkF8Gwg5jQzPl4LvoVmPdGJAqhWjbRWhZlBUiKqSoXRUUguQJiIm0JRsGr
g1QWC9wH3vL6VZz6ADARaXcl3QvEyJTXsddRdWvvfTZc3LyMAJNW9Z5QHRfhReI8SUxr1wLojLzAWjCT
8YnLnL0DJCbEbJBYA9gYImlEaxcDMqTMbj0FKHBMJR0HgcTl0lrdm2fOA8xHt0y0aJwGJHwrQXQCCdVa
7uH/Uf0fpw9jNbEjA/MAAAAASUVORK5CYII=
"""

def get_excel_icon(size=24):
    """Возвращает иконку Excel файла заданного размера"""
    return get_icon_from_base64(EXCEL_ICON, size)

def get_folder_icon(size=24):
    """Возвращает иконку папки заданного размера"""
    return get_icon_from_base64(FOLDER_ICON, size)

def get_icon_from_base64(base64_data, size=24):
    """Преобразует base64 строку в QIcon нужного размера"""
    # Декодируем base64 в бинарные данные
    image_data = base64.b64decode(base64_data)
    
    # Создаем QPixmap из бинарных данных
    pixmap = QPixmap()
    pixmap.loadFromData(QByteArray(image_data))
    
    # Масштабируем до нужного размера
    if size > 0:
        pixmap = pixmap.scaled(size, size)
        
    # Создаем и возвращаем QIcon
    return QIcon(pixmap)

def get_app_icon():
    """Возвращает иконку приложения (только для macOS)"""
    import sys
    import os
    
    # Проверяем, что мы на macOS
    if sys.platform == "darwin":
        icon_path = "pyqt_app/resources/icon.icns"
        if os.path.exists(icon_path):
            return QIcon(icon_path)
    
    # Для других платформ возвращаем пустую иконку
    return QIcon() 