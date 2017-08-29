print('Loading scraper.py')

from GoogleScraper import scrape_with_config
from bs4 import BeautifulSoup
from computer_vision import convert_image
from utils import is_english
from translate import *
import requests
import urllib
import random
import json
import re

config = {
  'use_own_ip': True,
  'keyword': 'placeholder',
  'search_engines': 'google',
  'num_pages_for_keyword': 1,
  'scrape_method': 'selenium',
  'sel_browser': 'phantomjs',
  'do_caching': False
}

def get_text_search_result(query):
  print('Searching [{}]'.format(query))
  global config
  config['keyword'] = query
  config['search_type'] = 'normal'
  config['search_engines'] = 'bing'
  try:
    search = scrape_with_config(config)
    serp = search.serps[0]
    if serp.status == 'successful':
      top_result = random.choice(serp.links)
      output = '\n'.join([top_result.link, top_result.title, '\n', str(top_result.snippet)])
  except Exception as e:
    print(e)
    output = '没搜到啊'
  return output

def get_image_search_result(query):
  print('Searching image [{}]'.format(query))
  global config
  config['keyword'] = query
  config['search_type'] = 'image'
  config['search_engines'] = 'yandex'

  try:
    search = scrape_with_config(config)
    serp = search.serps[0]
    top_result = random.choice(serp.links)
    url = top_result.link
    url = urllib.parse.unquote(url)
    content = requests.get(url).content
  except Exception as e:
    print(e)
    content = '没搜到啊'
  try:
    with open('tmp.jpg', 'wb') as f:
      f.write(content)
    info = convert_image('tmp.jpg', 'tmp.jpg')
  except:
    info = ''
  #return 'tmp.jpg'
  return '{} {}'.format(url, info) # for qq temporarily

reg_title = re.compile(r'<a class="js-title-link" href=(.*?)" target="_blank">(.*?)</a>')
reg_li = re.compile(r'item clearfix.*?')

def get_zhihu_search_result(keyword):
  print('Searching zhihu [{}]'.format(keyword))
  kw = urllib.parse.quote(keyword)
  url = 'https://www.zhihu.com/search?type=content&q={}'.format(kw)
  source = urllib.request.urlopen(url).read()
  print('source got')
  soup = BeautifulSoup(source, 'lxml')
  li = soup.find('li', {'class': reg_li})
  li = str(li)
  try:
    link, title = re.findall(reg_title, li)[0]
    title = title.replace('<em>', '')
    title = title.replace('</em>', '')
    return '{} {}'.format(link, title)
  except Exception as e:
    print(e)
  return '没找到啊'

def get_wikipedia_search_result(keyword):
  print('Searching [{}] on wikipedia'.format(keyword))
  try:
    url = 'https://en.wikipedia.org/w/index.php?search={}&title=Special:Search&profile=default&fulltext=1'.format(urllib.parse.quote(keyword))
    source = urllib.request.urlopen(url).read()
    print('source got')
    soup = BeautifulSoup(source, 'lxml')
    ul = soup.find('ul', {'class': 'mw-search-results'})
    li = ul.find('li')
    heading = li.find('div', {'class': 'mw-search-result-heading'}).find('a')
    link = urllib.parse.urljoin('https://en.wikipedia.org/', heading.get('href'))
    title = heading.text
    snippet = li.find('div', {'class': 'searchresult'}).text
    rtn = '{} {}\n\n{}'.format(link, title, snippet)
    return rtn
  except Exception as e:
    print(e)
    return '没找到啊'

def get_wolframalpha_search_result(keyword):
  print('Searching [{}] on wolframalpha'.format(keyword))
  rtn = ''
  if not is_english(keyword):
    keyword = get_translation_result(keyword)
    rtn += 'Did you mean {}?\n'.format(keyword)
  try:
    data = json.load(open('data.json', 'r'))
    app_id = data['APP_ID']
    url = 'http://api.wolframalpha.com/v1/result?' + urllib.parse.urlencode({'appid': app_id, 'i': keyword,'timeout': '5'})
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')
    rtn += soup.get_text()
    return rtn
  except Exception as e:
    print(e)
    rtn += '不知道怎么回答'
    return rtn

def get_emoji_search_result(keyword):
  print('Searching emoji {}'.format(keyword))
  try:
    kw = urllib.parse.quote(keyword)
    url = 'http://fabiaoqing.com/search/search/keyword/{}'.format(kw)
    print(url)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    images = [node['data-original'] for node in soup.select('img.bqppsearch')]
    image_url = random.choice(images)
    return image_url
  except Exception as e:
    print(e)
    return '没找到啊'
