import requests
import itchat
import os
import shutil
import re
import tensorflow as tf
import time
import itchat

from computer_vision import convert_image
from natural_language_processing import get_response
from utils import get_source

DEBUG = False

class Bot(object):
  def __init__(self):
    itchat.auto_login(hotReload=True, enableCmdQR=True)
    itchat.run()

@itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE], isGroupChat=True, isFriendChat=True)
def reply_message(msg):
  source = get_source(msg)
  print(msg)
  print(source)
  if source:
    if msg['Type'] == 'Text':
      content = msg['Text']
      if content.startswith(' '):
        print('Replying: ' + content)
        reply, status = get_response(content.strip())
        if status is True or status is False:
          global DEBUG
          DEBUG = not status
        reply = u'机器人: ' + reply
        global DEBUG
        if not DEBUG:
          itchat.send(reply, source)
        else:
          print('Sending {} to {}'.format(reply, source))
    elif msg['Type'] == 'Picture':
      filename = msg['FileName']
      msg['Text'](filename)
      shutil.move(filename, 'img/' + re.sub('.png', '.jpg', filename))
      try:
        start_time = time.time()
        info = convert_image('img/' + re.sub('.png', '.jpg', filename), 'tmp.jpg')
        print('{} seconds used for image classification'.format(time.time() - start_time))
        if info:
          print('output: ' + info)
          reply = u'机器人: ' + info
          global DEBUG
          if DEBUG:
            print('Sending {} to {}'.format(reply, source))
          else:
            itchat.send(reply, source)
      except:
        print('failed somewhere')
      # itchat.send_image('tmp.jpg', source)
  else:
    print('Ignored')
