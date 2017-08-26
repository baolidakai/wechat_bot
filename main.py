import requests
import itchat
import os
import shutil
import re
import tensorflow as tf
import json

from computer_vision import convert_image

DEBUG = False # Turn on DEBUG to suppress sending message, turn off to enable real message sending

survived = True

KEY = 'ca098ebe818b49df98af997bef29b3b3'

def get_response(content):
  if content == u'傻逼滚':
    global survived
    survived = False
    return u'我滚了'
  if content == u'傻逼回来':
    global survived
    survived = True
    return '我回来了'
  url = 'http://www.tuling123.com/openapi/api'
  data = {
      'key': KEY,
      'info': content,
      'userid': 'pth-robot',
  }
  try:
    r = requests.post(url, data=data).json()
    return r.get('text')
  except:
    pass

user_data = json.load(open('data.json', 'r'))
trigger_nicknames = user_data['trigger_nicknames']
trigger_usernames = user_data['trigger_usernames']
myself_username = user_data['myself_username']

# Return the source user to reply to, none if no need to reply
def get_source(msg):
  if msg['FromUserName'] == myself_username and msg['ToUserName'].startswith('@@'): # my message in a group chat
    print('my message to a group')
    return msg['ToUserName']
  elif msg['FromUserName'].startswith('@@') and msg['ActualNickName'] in trigger_nicknames and msg['ToUserName'] == myself_username: # group chat message sent to me from a whitelist user
    print('group message to me')
    return msg['FromUserName']
  elif msg['FromUserName'] == myself_username and msg['ToUserName'] in trigger_usernames: # my private message to whitelist user
    print('my message to friend')
    return msg['ToUserName']
  elif msg['FromUserName'] in trigger_usernames and msg['ToUserName'] == myself_username: # private message from whitelist user to myself
    print('friend message to me')
    return msg['FromUserName']
  return None

@itchat.msg_register([itchat.content.TEXT], isGroupChat=True, isFriendChat=True)
def reply_message(msg):
  source = get_source(msg)
  print(msg)
  print(source)
  if source:
    content = msg['Text']
    if content.startswith(' '):
      print('Replying: ' + content)
      defaultReply = u'不知道该说什么好'
      if survived:
        reply = get_response(content.strip())
        reply = reply or defaultReply
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
      info = convert_image('img/' + re.sub('.png', '.jpg', filename), 'tmp.jpg')
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
