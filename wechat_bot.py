import requests
import os
import shutil
import re
import tensorflow as tf
import time
import itchat

from computer_vision import convert_image
from natural_language_processing import get_response
from utils import get_source

DEBUG = True

class WechatBot(object):
  def __init__(self):
    itchat.auto_login(hotReload=True)
    itchat.run()

@itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE], isGroupChat=True, isFriendChat=True)
def reply_message(msg):
  global DEBUG
  source = get_source(msg)
  print(msg)
  print(source)
  rtn = dict() # dictionary to store the actions
  if source:
    if msg['Type'] == 'Text':
      content = msg['Text']
      if content.startswith(' '):
        print('Received: ' + content)
        reply, status = get_response(content.strip())
        if not reply:
          print('Getting no response')
          return rtn
        if status is True or status is False:
          DEBUG = not status
        if reply == 'tmp.jpg':
          if not DEBUG:
            itchat.send_image('tmp.jpg', source)
          else:
            print('Sending image tmp.jpg to {}'.format(source))
          rtn['image'] = ('tmp.jpg', source)    
          return rtn
        reply = u'机器人: ' + reply
        if not DEBUG:
          itchat.send(reply, source)
        else:
          print('Sending {} to {}'.format(reply, source))
        rtn['text'] = (reply, source)
        return rtn
    elif msg['Type'] == 'Picture':
      filename = msg['FileName']
      try:
        msg['Text'](filename)
        shutil.move(filename, 'img/' + re.sub('.png', '.jpg', filename))
      except Exception as e:
        print(e)
      try:
        start_time = time.time()
        info = convert_image('img/' + re.sub('.png', '.jpg', filename), 'tmp.jpg')
        print('{} seconds used for image classification'.format(time.time() - start_time))
        if info:
          print('output: ' + info)
          reply = u'机器人: ' + info
          if DEBUG:
            print('Sending {} to {}'.format(reply, source))
          else:
            itchat.send(reply, source)
          rtn['text'] = (reply, source)
          return rtn
      except Exception as e:
        print(e)
  else:
    print('Ignored')
  return rtn
