from xvfbwrapper import Xvfb
from selenium import webdriver
import time

hair_style_dict = {
  'long': 'Long Hair',
  'short': 'Short Hair',
  'twin': 'Twin Tail',
  'drill': 'Drill Hair',
  'ponytail': 'Ponytail'
}

def parse_message_to_options(msg):
  user_options = {
    'hair_color': 'Random',
    'hair_style': 'Random',
    'eye_color': 'Random',
    'blush': 'Random',
    'smile': 'Random',
    'open_mouth': 'Random',
    'hat': 'Random',
    'ribbon': 'Random',
    'glasses': 'Random'
  }
  for option in ['blush', 'smile', 'hat', 'ribbon', 'glasses']:
    if 'no ' + option in msg:
      user_options[option] = 'Off'
    elif option in msg:
      user_options[option] = 'On'
  if 'close mouth' in msg:
    user_options['open_mouth'] = 'Off'
  elif 'open mouth' in msg:
    user_options['open_mouth'] = 'On'
  for hair_style_option in ['long', 'short', 'twin', 'drill', 'ponytail']:
    if hair_style_option in msg:
      user_options['hair_style'] = hair_style_dict[hair_style_option]
  for color_option in ['blonde', 'brown', 'black', 'blue', 'pink', 'purple', 'green', 'red', 'silver', 'white', 'orange', 'aqua', 'grey']:
    if color_option + ' hair' in msg:
      user_options['hair_color'] = color_option.capitalize()
    if color_option + ' eye' in msg:
      user_options['eye_color'] = color_option.capitalize()
  return user_options

def get_girl(msg):
  display = Xvfb(width=1200, height=600, colordepth=16)
  display.start()
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('window-size=1200x600')
  chrome_options.add_argument('--no-sandbox')
  driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
  
  print('Getting website')
  driver.get('http://make.girls.moe/')
  driver.get_screenshot_as_file('../www/debug.png')
  print('Got')
  
  xpath_dict = {
    'hair_color': '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div',
    'hair_style': '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div',
    'eye_color': '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div[3]/div',
    'blush': '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div[1]/div',
    'smile': '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div[2]/div',
    'open_mouth': '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div[3]/div',
    'hat': '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div[4]/div',
    'ribbon': '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div[5]/div',
    'glasses': '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div[6]/div',
    'generate_btn': '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[1]/div/button',
    'image': '//*[@id="root"]/div/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/img',
    'progress': '//*[@id="root"]/div/div/div/div/div[1]/div[1]'
  }
  
  user_options = parse_message_to_options(msg)
  print(user_options)

  # Check connectivity
  progress = driver.find_element_by_xpath(xpath_dict['progress'])
  print(progress)
  print(progress.text)
  if 'Network Error' in progress.text:
    driver.get_screenshot_as_file('../www/debug.png')
    driver.close()
    display.stop()
    return 'Network error'
  
  # Select options
  for option, choice in user_options.items():
    try:
      xpath = xpath_dict[option]
      element = driver.find_element_by_xpath(xpath)
      element.click()
      try:
        subelement = element.find_elements_by_link_text(choice)[0]
      except:
        subelements = element.find_elements_by_class_name('btn')
        choices = element.text.split('\n')
        subelement = subelements[choices.index(choice)]
      subelement.click()
      print('Element clicked')
      print('Saving screenshot')
      driver.get_screenshot_as_file('../www/debug.png')
    except Exception as e:
      print(e)
      print('Unable to select {} for {}'.format(choice, option))
  
  image_src = None
  clicked = False
  for i in range(20):
    print('Waiting for 1 second')
    time.sleep(5)
    try:
      print('Trying to download the image')
      print('Trying to click the generate button')
      generate_btn = driver.find_element_by_xpath(xpath_dict['generate_btn'])
      print(generate_btn)
      if generate_btn.is_enabled() and not clicked:
        generate_btn.click()
        clicked = True
        print('Button clicked')
      if clicked:
        print('Button clicked')
      image = driver.find_element_by_xpath(xpath_dict['image'])
      image_src = image.get_attribute('src')
      print('Successful')
      break
    except Exception as e:
      print('Failed for the {} th time'.format(i))
      print(e)
    finally:
      driver.get_screenshot_as_file('../www/debug.png')
  
  with open('../www/animation.html', 'w') as f:
    f.write('<img src="{}"/>'.format(image_src))
    print('Writing result image to animation.html')
  
  driver.close()
  display.stop()

  return 'http://www.bowendeng.com/animation.html' if image_src else 'failed'
