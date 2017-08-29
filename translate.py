import translation
import string

def is_english(s):
  try:
    s.encode(encoding='utf-8').decode('ascii')
  except UnicodeDecodeError:
    return False
  else:
    return True

def get_translation_result(query):
  dst_lang = 'zh-CHS' if is_english(query) else 'en'
  rtn = translation.bing(query, dst=dst_lang)
  return rtn
