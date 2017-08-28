from bot import *

msg1 = { # Should not trigger anything
  'Type': 'Text',
  'Text': 'hello',
  'FromUserName': '@14341204faee8b10343b43632b7aa83163b81c64e04825c7df32480d9d16a63a',
  'ToUserName': '@@fake_group_id'
}

msg2 = { # Should trigger a reply
  'Type': 'Text',
  'Text': ' hello',
  'FromUserName': '@14341204faee8b10343b43632b7aa83163b81c64e04825c7df32480d9d16a63a',
  'ToUserName': '@@fake_group_id'
}

msg3 = { # Should trigger manual rule
  'Type': 'Text',
  'Text': ' 你好',
  'FromUserName': '@14341204faee8b10343b43632b7aa83163b81c64e04825c7df32480d9d16a63a',
  'ToUserName': '@@fake_group_id'
}

msg4 = { # Should recognize as a lion
  'Type': 'Picture',
  'FileName': 'lion.jpg',
  'FromUserName': '@14341204faee8b10343b43632b7aa83163b81c64e04825c7df32480d9d16a63a',
  'ToUserName': '@@fake_group_id'
}

msg5 = { # Should trigger text search
  'Type': 'Text',
  'Text': ' 搜索 你好世界',
  'FromUserName': '@14341204faee8b10343b43632b7aa83163b81c64e04825c7df32480d9d16a63a',
  'ToUserName': '@@fake_group_id'
}

msg6 = { # Should trigger image search
  'Type': 'Text',
  'Text': ' 搜图 little lion',
  'FromUserName': '@14341204faee8b10343b43632b7aa83163b81c64e04825c7df32480d9d16a63a',
  'ToUserName': '@@fake_group_id'
}

output1 = reply_message(msg1)
expected1 = {}
assert output1 == expected1

output2 = reply_message(msg2)
assert output2['text'][1] == '@@fake_group_id'

output3 = reply_message(msg3)
expected3 = {'text': ('机器人: 你好', '@@fake_group_id')}
assert output3 == expected3

output4 = reply_message(msg4)
assert output4['text'][1] == '@@fake_group_id' and 'lion' in output4['text'][0]

output5 = reply_message(msg5)
assert output5['text'][1]== '@@fake_group_id' and '你好世界' in output5['text'][0]

output6 = reply_message(msg6)
expected6 = {'image': ('tmp.jpg', '@@fake_group_id')}
assert output6 == expected6
