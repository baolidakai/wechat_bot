import requests
import itchat
import os
import shutil
import re
import tensorflow as tf
import time

from computer_vision import convert_image
from natural_language_processing import get_response
from utils import get_source

DEBUG = False # Turn on DEBUG to suppress sending message, turn off to enable real message sending

survived = True

@itchat.msg_register([itchat.content.TEXT], isGroupChat=True, isFriendChat=True)
def reply_message(msg):
  source = get_source(msg)
  print(msg)
  print(source)
  if source:
    content = msg['Text']
    if content.startswith(' '):
      print('Replying: ' + content)
      if survived:
        reply, status = get_response(content.strip())
        if status is True:
          global survived
          survived = True
        if status is False:
          global survived
          survived = False
        reply = u'机器人: ' + reply
        if DEBUG:
          print('Sending {} to {}'.format(reply, source))
        else:
          itchat.send(reply, source)
  else:
    print('Ignored')


@itchat.msg_register([itchat.content.PICTURE], isGroupChat=True, isFriendChat=True)
def get_pic(msg):
  source = get_source(msg)
  print(msg)
  print(source)
  if source:
    filename = msg['FileName']
    msg['Text'](filename)
    shutil.move(filename, 'img/' + re.sub('.png', '.jpg', filename))
    try:
      start_time = time.time()
      info = convert_image('img/' + re.sub('.png', '.jpg', filename), 'tmp.jpg')
      print('{} seconds used for image classification'.format(time.time() - start_time))
      if info:
        print('output: ' + info)
        if survived:
          reply = u'机器人: ' + info
          if DEBUG:
            print('Sending {} to {}'.format(reply, source))
          else:
            itchat.send(reply, source)
    except:
      print('failed somewhere')
    # itchat.send_image('tmp.jpg', source)
  else:
    print('Ignored')

itchat.auto_login(hotReload=True)
itchat.run()
