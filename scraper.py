from GoogleScraper import scrape_with_config, GoogleSearchError

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
  try:
    search = scrape_with_config(config)
    serp = search.serps[0]
    if serp.status == 'successful':
      top_result = serp.links[0]
      output = '\n'.join([top_result.link, top_result.title, '\n', top_result.snippet])
  except:
    print('Failed')
    output = None
  return output
