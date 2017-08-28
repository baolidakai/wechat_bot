import requests
import os
import shutil
import re
import tensorflow as tf
import time
import itchat

# from computer_vision import convert_image
from natural_language_processing import get_response

from qqbot import _bot as bot
from qqbot import QQBotSlot as qqbotslot, RunBot

bot.Login(['-q', '1234'])

group = bot.List('group', '机器人')[0]
members = [member.name for member in bot.List(group)]

@qqbotslot
def onQQMessage(bot, contact, member, content):
  if contact.name == group.name and member.name in members and content.startswith(' '):
    content = content.strip()
    try:    
      reply, status = get_response(content)
    except:
      reply = '失败了/哭'
    print('Sending @{} {}'.format(member.name, reply))
    bot.SendTo(contact, '@{} {}'.format(member, reply))
  else:
    print('Ignoring')
    print(contact)
    print(member)
    print(content)

RunBot()
