Wechat robot for fun

## Prerequisites
* Get free api key on http://www.tuling123.com/member/center/
* Get free app id on https://developer.wolframalpha.com/portal/myapps/index.html
* tensorflow
* itchat
* Install phantomjs https://www.vultr.com/docs/how-to-install-phantomjs-on-ubuntu-16-04
* Install tensorflow models inside this repository. See https://github.com/tensorflow/models/tree/master/slim.
* Download http://download.tensorflow.org/models/inception\_v3\_2016\_08\_28.tar.gz and unzip inside pre\_trained
* Install https://github.com/NikolaiT/GoogleScraper
* Add a file named data.json which stores something like:
{
    "API_KEY": "exampleapikey",
    "APP_ID": "exampleapiid",
	"trigger_nicknames": ["邓博文", ...],
	"trigger_usernames": [
	  "@myusername",
      "@myfriendusername"
	],
	"myself_username": "@myusername"
}
where API\_KEY is the free app id for walfram alpha
* Add a file named rules.json which stores manual rules like:
{
	"名字": "小歪",
	"星座": "巨蟹座"
}

## Functionaliy
* reply chat message if you add 小歪 before the message [小歪你好]
* return top web search result if you use the syntax [小歪搜索 cat]
* search image if you use the syntax [小歪搜图 cat]
* search on zhihu and return top result if you use the syntax [小歪搜知乎 cat]
* search on wikipedia if you use the syntax [小歪搜wiki cat]
* search emoji if you use the syntax [小歪搜表情 cat]
* chat with wolframalpha if you use the syntax [小歪英文 cat]
* recognize object inside an image if you send an image (only available on wechat)

## TODOs
* Add teach you functionality
* Add logic understanding
* Add notification functionality

## File System
utils.py: various utility methods
rules.json: hand-written text replies
computer\_vision.py: computer vision program which returns image label
natural\_language\_processing.py: nlp program which returns a reply given a text message
models: directory containing the tensorflow/models module
pre\_trained: directory which stores the model ckpt
data.json: json file containing all private data

## Examples
