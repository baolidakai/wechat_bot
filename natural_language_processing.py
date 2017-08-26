import requests
import json

from scraper import get_text_search_result

API_KEY = 'ca098ebe818b49df98af997bef29b3b3'

# key is the trigger word for the feature, value is the corresponding function to use
special_feature_dict = {
  u'搜索': get_text_search_result
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
      return func(content), None
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
