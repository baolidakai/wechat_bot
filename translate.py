import translation
from utils import is_english

def get_translation_result(query):
  dst_lang = 'zh-CHS' if is_english(query) else 'en'
  rtn = translation.bing(query, dst=dst_lang)
  return rtn
