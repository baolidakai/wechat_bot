from GoogleScraper import scrape_with_config, GoogleSearchError
import urllib
import requests

config = {
  'use_own_ip': True,
  'keyword': 'placeholder',
  'search_engines': ['google'],
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
  config['search_engines'] = 'google'
  try:
    search = scrape_with_config(config)
    serp = search.serps[0]
    if serp.status == 'successful':
      top_result = serp.links[0]
      output = '\n'.join([top_result.link, top_result.title, '\n', str(top_result.snippet)])
  except Exception as e:
    print(e)
    output = None
  return output

def get_image_search_result(query):
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
    return None
  try:
    with open('tmp.jpg', 'wb') as f:
      f.write(content)
  except:
    return None
  return 'tmp.jpg'
