print('Loading qq_bot.py')

import requests
import os
import shutil
import re
import tensorflow as tf
import time
import itchat

from natural_language_processing import get_response

#from qqbot import _bot as bot
from qqbot import QQBotSlot as qqbotslot, RunBot

#bot.Login(['-q', '1234'])

DEBUG = False
BUDGET = 100

@qqbotslot
def onQQMessage(bot, contact, member, content):
  global DEBUG
  global BUDGET
  if contact.name == '机器人' and content.startswith('小歪'):
    content = content[2:]
    try:    
      reply, status = get_response(content)
    except Exception as e:
      print(e)
      reply = '失败了/哭'
      status = None
    print('Sending @{} {}'.format(member.name, reply))
    if status is True:
      DEBUG = False
    if not DEBUG and BUDGET > 0:
      BUDGET -= 1
      print('{} messages left'.format(BUDGET))
      if reply:
        bot.SendTo(contact, '@{} {}'.format(member, reply))
    elif BUDGET == 0:
      print('message limit exceeded')
      bot.SendTo(contact, '@{} 我不能再发消息了'.format(member))
    if status is False:
      DEBUG = True
  else:
    print('Ignoring')
    print(contact)
    print(member)
    print(content)

RunBot()
