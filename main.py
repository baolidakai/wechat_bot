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

trigger_user = {u'@@b7326c0e23562a9cfb91992aa881e5fcda2b167f4ac699cb907f8745938b0c17'} # this is our group chat

@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)
def reply_message(msg):
  source = None
  if msg['ToUserName'] in trigger_user:
    source = msg['ToUserName']
  if msg['FromUserName'] in trigger_user:
    source = msg['FromUserName']
  if source:
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
  source = None
  if msg['ToUserName'] in trigger_user:
    source = msg['ToUserName']
  if msg['FromUserName'] in trigger_user:
    source = msg['FromUserName']
  if source:
    filename = msg['FileName']
    msg['Text'](filename)
    shutil.move(filename, 'img/' + re.sub('.png', '.jpg', filename))
    info = convert_image('img/' + re.sub('.png', '.jpg', filename), 'tmp.jpg')
    if info:
      itchat.send(u'机器人: ' + info, source)
    itchat.send_image('tmp.jpg', source)
  else:
    print(msg['ToUserName'])
    print(msg['FromUserName'])


itchat.auto_login(hotReload=True)
itchat.run()
