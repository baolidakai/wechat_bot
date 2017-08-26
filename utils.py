# Return the source user to reply to, none if no need to reply
import json

def get_source(msg):
  user_data = json.load(open('data.json', 'r'))
  trigger_nicknames = user_data['trigger_nicknames']
  trigger_usernames = user_data['trigger_usernames']
  myself_username = user_data['myself_username']
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
