from chardet.universaldetector import UniversalDetector
import os
import requests


def translate_it(text):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    # key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
    key = 'trnsl.1.1.20161214T114634Z.0492e7b1ebd2d3b4.57c088043e2306103d52f62d96bbf3893cac7554'

    params = {
        'key': key,
        'lang': 'en-ru',
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))


def translate_it_ext(file_from, file_to, lang_from, lang_to='ru'):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161214T114634Z.0492e7b1ebd2d3b4.57c088043e2306103d52f62d96bbf3893cac7554'
    file_encoding = get_encoding_from_file(file_from)["encoding"]
    with open(file_from, encoding=file_encoding) as f:
        text = f.read()
    params = {
        'key': key,
        'lang': '-'.join((lang_from, lang_to)),
        'text': text,
    }
    response = requests.get(url, params=params).json()
    with open(file_to, 'w') as f:
        f.write(' '.join(response.get('text', [])))


def get_files(ext, excluding):
    result = []
    for name in os.listdir("./"):
        if name.endswith("." + ext) and not excluding.lower() in name.lower():
            result.append(name)
    return result


def get_encoding_from_files(files):
    result = {}
    for name in files:
        result[name] = get_encoding_from_file(name)
    return result


def get_encoding_from_file(file):
    detector = UniversalDetector()
    with open(file, 'rb') as fh:
        for line in fh:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result


def get_lang(text):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
    key = 'trnsl.1.1.20161214T114634Z.0492e7b1ebd2d3b4.57c088043e2306103d52f62d96bbf3893cac7554'
    params = {
        'key': key,
        'text': text
    }
    response = requests.get(url, params=params).json()
    return response.get('lang')


if __name__ == '__main__':
    files = get_files('txt', '-ru')
    encodings = get_encoding_from_files(files)
    for file_from, result_encoding in encodings.items():
        with open(file_from, encoding=result_encoding["encoding"]) as f:
            text = f.read()
            lang_from = get_lang(text)
            lang_to = 'ru'
            file_name = os.path.splitext(file_from)[0]
            ext = os.path.splitext(file_from)[1]
            file_to = file_name + '-' + lang_to + ext
            translate_it_ext(file_from, file_to, lang_from, lang_to)
