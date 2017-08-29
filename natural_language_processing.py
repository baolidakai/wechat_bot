import requests
import json

from scraper import *
from translate import *

data = json.load(open('data.json', 'r'))
API_KEY = data['API_KEY']

# key is the trigger word for the feature, value is the corresponding function to use
special_feature_dict = {
  u'搜索': get_text_search_result,
  u'搜图': get_image_search_result,
  u'搜知乎': get_zhihu_search_result,
  u'搜wiki': get_wikipedia_search_result,
  u'翻译': get_translation_result
}

# Given the content in a string, return the response and 
def get_response(content):
  rules = json.load(open('rules.json', 'r'))
  if content == u'傻逼滚':
    return u'我滚了', False
  if content == u'傻逼回来':
    return u'我回来了', True
  if content in rules:
    print('Using hand written rule {}=>{}'.format(content, rules[content]))
    return rules[content], None
  # Trigger special feature
  for trigger, func in special_feature_dict.items():
    if content.startswith(trigger):
      content = content[len(trigger) + 1:]
      reply = func(content)
      return reply, None
  url = 'http://www.tuling123.com/openapi/api'
  data = {
      'key': API_KEY,
      'info': content,
      'userid': 'pth-robot',
  }
  try:
    r = requests.post(url, data=data).json()
    return r.get('text'), None
  except:
    return u'我断网了', None
