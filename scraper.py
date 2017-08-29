from GoogleScraper import scrape_with_config
from bs4 import BeautifulSoup
from computer_vision import convert_image
import urllib
import requests
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
      top_result = serp.links[0]
      output = '\n'.join([top_result.link, top_result.title, '\n', str(top_result.snippet)])
  except Exception as e:
    print(e)
    output = ''
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
    top_result = serp.links[0]
    url = top_result.link
    url = urllib.parse.unquote(url)
    content = requests.get(url).content
  except Exception as e:
    print(e)
    content = ''
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
  return ''
