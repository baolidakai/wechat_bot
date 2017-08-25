import requests
import itchat
import os
import shutil
import re
import tensorflow as tf

from computer_vision import convert_image

survived = True

KEY = 'ca098ebe818b49df98af997bef29b3b3'

def get_response(msg):
  if msg == u'你喜欢我吗':
    return u'{}我喜欢你'.format(msg['ActualNickName'])
  if msg == u'傻逼滚':
    global survived
    survived = False
    return u'我滚了'
  if msg == u'傻逼回来':
    global survived
    survived = True
    return '我回来了'
  url = 'http://www.tuling123.com/openapi/api'
  data = {
      'key': KEY,
      'info': msg,
      'userid': 'pth-robot',
  }

  try:
    r = requests.post(url, data=data).json()
    return r.get('text')
  except:
    pass

trigger_nicknames = {u'邓博文', u'Bao Qi', u'小七'}

def get_source(msg):
  if msg['ToUserName'].startswith('@@'):
    return msg['ToUserName']
  if msg['FromUserName'].startswith('@@'):
    return msg['FromUserName']
  return None

@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)
def reply_message(msg):
  if msg['ActualNickName'] not in trigger_nicknames:
    print('Ignoring this message')
    print(msg)
    return
  source = get_source(msg)
  if source:
    print(source)
    content = msg['Text']
    if content.startswith(' '):
      print('Replying: ' + content)
      defaultReply = u'不知道该说什么好'
      if survived:
        reply = get_response(msg['Text'].strip())
        reply = reply or defaultReply
        reply = u'机器人: ' + reply
        itchat.send(reply, source)
  print(msg)


@itchat.msg_register([itchat.content.PICTURE], isGroupChat=True)
def get_pic(msg):
  if msg['ActualNickName'] not in trigger_nicknames:
    print('Ignoring this message')
    print(msg)
    return
  source = get_source(msg)
  if source:
    filename = msg['FileName']
    msg['Text'](filename)
    shutil.move(filename, 'img/' + re.sub('.png', '.jpg', filename))
    try:
      info = convert_image('img/' + re.sub('.png', '.jpg', filename), 'tmp.jpg')
      if info:
        print('output: ' + info)
        itchat.send(u'机器人: ' + info, source)
    except:
      print('failed somewhere')
    # itchat.send_image('tmp.jpg', source)
  print(msg)


itchat.auto_login(hotReload=True)
itchat.run()
