Wechat robot for fun

The current text response is from tuling robot.

Working on image classification

## Prerequisites
* tensorflow
* itchat
* Install phantomjs https://www.vultr.com/docs/how-to-install-phantomjs-on-ubuntu-16-04
* Install tensorflow models inside this repository. See https://github.com/tensorflow/models/tree/master/slim.
* Download http://download.tensorflow.org/models/inception\_v3\_2016\_08\_28.tar.gz and unzip inside pre\_trained
* Install https://github.com/NikolaiT/GoogleScraper
* Add a file named data.json which stores something like:
{
	"trigger_nicknames": ["邓博文", ...],
	"trigger_usernames": [
	  "@14341204faee8b10343b43632b7aa83163b81c64e04825c7df32480d9d16a63a",
	  ...
	],
	"myself_username": "@14341204faee8b10343b43632b7aa83163b81c64e04825c7df32480d9d16a63a"
}
* Add a file named rules.json which stores manual rules like:
{
	"名字": "小歪",
	"星座": "巨蟹座"
}

## Functionaliy
* reply chat message if you add a whitespace before the text
* recognize object inside an image if you send an image

## TODOs
* Add notification functionality
* Search on wikipedia
* Enable question answering using wolfram alpha api https://www.yangzhou301.com/2017/05/21/514548234/
* Enable emoji
* Add teach you functionality
* Add logic understanding

## File System
utils.py: various utility methods
rules.json: hand-written text replies
computer\_vision.py: computer vision program which returns image label
natural\_language\_processing.py: nlp program which returns a reply given a text message
models: directory containing the tensorflow/models module
pre\_trained: directory which stores the model ckpt
data.json: json file containing all private data
