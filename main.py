import requests
import itchat

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

trigger_user = {u'@@fa4298c09bd6ab30496e45ec549a325250e47ee6d6726e681de81c99ee758438'} # this is our group chat

@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)
def reply_message(msg):
  source = None
  print(msg)
  if msg['ToUserName'] in trigger_user:
    source = msg['ToUserName']
  if msg['FromUserName'] in trigger_user:
    source = msg['FromUserName']
  content = msg['Text']
  if source and content.startswith(' '):
    defaultReply = 'I received: ' + msg['Text']
    if survived:
      reply = get_response(msg['Text'])
      reply = reply or defaultReply
      reply = u'机器人: ' + reply
      itchat.send(reply, source)

itchat.auto_login(hotReload=True)
itchat.run()
