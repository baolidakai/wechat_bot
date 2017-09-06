# Return the source user to reply to, none if no need to reply
import time
import json
import string

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

def is_english(s):
  try:
    s.encode(encoding='utf-8').decode('ascii')
  except UnicodeDecodeError:
    return False
  else:
    return True

def send_notification(delay, msg, bot, contact, member, DEBUG):
  print('Will send message {} after {} seconds'.format(msg, delay))
  if not DEBUG:
    bot.SendTo(contact, '@{} I will notify you after {} seconds'.format(member, delay))
  time.sleep(delay)
  print('{} seconds passed, sending message {}'.format(delay, msg))
  if not DEBUG:
    bot.SendTo(contact, '@{} {}'.format(member, msg))

def to_second(delay):
  rtn = 0
  if 'h' in delay:
    try:
      num_hours = int(delay.split('h')[0])
      delay = delay.split('h')[1]
      rtn += num_hours * 3600
    except:
      pass
  if 'm' in delay:
    try:
      num_minutes = int(delay.split('m')[0])
      delay = delay.split('m')[1]
      rtn += num_minutes * 60
    except:
      pass
  if 's' in delay:
    try:
      num_seconds = int(delay.split('s')[0])
      delay = delay.split('s')[1]
      rtn += num_seconds
    except:
      pass
  return rtn
