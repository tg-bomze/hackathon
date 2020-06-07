# https://cloud.yandex.ru/docs/translate/
import json
import requests
from datetime import datetime, timedelta

global data
with open('data.json') as f:
    data = json.load(f)

#oauth_token = "AgAAAAATXuCbAATuwds6JLx1SU-jmDBVyQU1Qjk"
#folderId = "b1g6l7gmil55de5s7snq"
#langs = [{'code': 'az', 'name': 'azərbaycan'}, {'code': 'sq', 'name': 'shqip'}, {'code': 'am', 'name': 'አማርኛ'}, {'code': 'en', 'name': 'English'}, {'code': 'ar', 'name': 'العربية'}, {'code': 'hy', 'name': 'հայերեն'}, {'code': 'af', 'name': 'Afrikaans'}, {'code': 'eu', 'name': 'euskara'}, {'code': 'ba'}, {'code': 'be', 'name': 'беларуская'}, {'code': 'bn', 'name': 'বাংলা'}, {'code': 'my', 'name': 'မြန်မာ'}, {'code': 'bg', 'name': 'български'}, {'code': 'bs', 'name': 'bosanski'}, {'code': 'cy', 'name': 'Cymraeg'}, {'code': 'hu', 'name': 'magyar'}, {'code': 'vi', 'name': 'Tiếng Việt'}, {'code': 'ht'}, {'code': 'gl', 'name': 'galego'}, {'code': 'nl', 'name': 'Nederlands'}, {'code': 'el', 'name': 'Ελληνικά'}, {'code': 'ka', 'name': 'ქართული'}, {'code': 'gu', 'name': 'ગુજરાતી'}, {'code': 'da', 'name': 'dansk'}, {'code': 'he', 'name': 'עברית'}, {'code': 'yi', 'name': 'ייִדיש'}, {'code': 'id', 'name': 'Indonesia'}, {'code': 'ga', 'name': 'Gaeilge'}, {'code': 'it', 'name': 'italiano'}, {'code': 'is', 'name': 'íslenska'}, {'code': 'es', 'name': 'español'}, {'code': 'kk', 'name': 'қазақ тілі'}, {'code': 'kn', 'name': 'ಕನ್ನಡ'}, {'code': 'ca', 'name': 'català'}, {'code': 'ky', 'name': 'кыргызча'}, {'code': 'zh', 'name': '中文'}, {'code': 'ko', 'name': '한국어'}, {'code': 'xh'}, {'code': 'km', 'name': 'ខ្មែរ'}, {'code': 'lo', 'name': 'ລາວ'}, {'code': 'la'}, {'code': 'lv', 'name': 'latviešu'}, {'code': 'lt', 'name': 'lietuvių'}, {'code': 'lb', 'name': 'Lëtzebuergesch'}, {'code': 'mg', 'name': 'Malagasy'}, {'code': 'ms', 'name': 'Melayu'}, {'code': 'ml', 'name': 'മലയാളം'}, {'code': 'mt', 'name': 'Malti'}, {'code': 'mk', 'name': 'македонски'}, {'code': 'mi'}, {'code': 'mr', 'name': 'मराठी'}, {'code': 'mn', 'name': 'монгол'}, {'code': 'de', 'name': 'Deutsch'}, {'code': 'ne', 'name': 'नेपाली'}, {'code': 'no', 'name': 'norsk bokmål'}, {'code': 'pa', 'name': 'ਪੰਜਾਬੀ'}, {'code': 'fa', 'name': 'فارسی'}, {'code': 'pl', 'name': 'polski'}, {'code': 'pt', 'name': 'português'}, {'code': 'ro', 'name': 'română'}, {'code': 'ru', 'name': 'русский'}, {'code': 'sr', 'name': 'српски'}, {'code': 'si', 'name': 'සිංහල'}, {'code': 'sk', 'name': 'slovenčina'}, {'code': 'sl', 'name': 'slovenščina'}, {'code': 'sw', 'name': 'Kiswahili'}, {'code': 'su'}, {'code': 'tg', 'name': 'тоҷикӣ'}, {'code': 'th', 'name': 'ไทย'}, {'code': 'tl', 'name': 'Filipino'}, {'code': 'ta', 'name': 'தமிழ்'}, {'code': 'tt', 'name': 'татар'}, {'code': 'te', 'name': 'తెలుగు'}, {'code': 'tr', 'name': 'Türkçe'}, {'code': 'uz', 'name': 'o‘zbek'}, {'code': 'uk', 'name': 'українська'}, {'code': 'ur', 'name': 'اردو'}, {'code': 'fi', 'name': 'suomi'}, {'code': 'fr', 'name': 'français'}, {'code': 'hi', 'name': 'हिन्दी'}, {'code': 'hr', 'name': 'hrvatski'}, {'code': 'cs', 'name': 'čeština'}, {'code': 'sv', 'name': 'svenska'}, {'code': 'gd', 'name': 'Gàidhlig'}, {'code': 'et', 'name': 'eesti'}, {'code': 'eo', 'name': 'esperanto'}, {'code': 'jv'}, {'code': 'ja', 'name': '日本語'}]

text = ["Россия Вперед", "Можем повторить!", "Спасибо деду за победу"]
lang_in = "ru"
lang_out = "en"

def create_token(oauth_token):
    params = {'yandexPassportOauthToken': oauth_token}
    response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', params=params)                                                   
    #print(response) # https://cloud.yandex.ru/docs/translate/api-ref/errors-handling
    decode_response = response.content.decode('UTF-8')
    text = json.loads(decode_response) 
    iam_token = text.get('iamToken')
    expires_iam_token = text.get('expiresAt')
    return iam_token, expires_iam_token

def list_lang(access_token, folderId):
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/languages',
                       headers={'Content-Type':'application/json',
                                'Authorization': 'Bearer {}'.format(access_token)},
                       json = {"folderId": folderId})
    #print(response) # https://cloud.yandex.ru/docs/translate/api-ref/errors-handling
    decode_response = response.content.decode('UTF-8')
    text = json.loads(decode_response)
    return text

def translate(access_token, lang_in, lang_out, text, folderId):
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                       headers={'Content-Type':'application/json',
                                'Authorization': 'Bearer {}'.format(access_token)},
                       json = {"sourceLanguageCode": lang_in,
                                  "targetLanguageCode": lang_out,
                                  "format": "PLAIN_TEXT",
                                  "texts": text,
                                  "folderId": folderId})
    #print(response) # https://cloud.yandex.ru/docs/translate/api-ref/errors-handling
    decode_response = response.content.decode('UTF-8')
    text = json.loads(decode_response)
    translations_json = text.get('translations')
    translations = []
    for i in range(len(translations_json)):
        translations.append(translations_json[i].get('text'))
    return translations

'''end_time = datetime.strptime(data["end_time"],'%Y-%m-%dT%H:%M:%S.%fZ')
if datetime.now() > end_time:
	data["access_token"], data["end_time"] = create_token(data["oauth_token"])
	langs = list_lang(data["access_token"], data["folderId"])
	with open('data.json', 'w') as f: json.dump(data, f, sort_keys=True, indent=4)
	print("Токен успешно сгенерирован и действует до {}\n".format(data["end_time"]))

end_time = datetime.strptime(data["end_time"],'%Y-%m-%dT%H:%M:%S.%fZ')
if datetime.now() <= end_time:
	trans = translate(data["access_token"], lang_in, lang_out, text, data["folderId"])
	for i in range(len(trans)):
		print("{} ({}) - {} ({})".format(text[i], lang_in, trans[i], lang_out))'''
