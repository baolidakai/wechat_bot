Wechat robot for fun

Currently it works in a single group chat. Replace the trigger\_user set with a set of group chat ids you want to make it work.

The current text response is from tuling robot.

Working on image classification

## Prerequisites
* Edit ~/.config/ipython/profile\_default/startup/ipython3\_startup.ipy and put
%load\_ext autoreload
%autoreload 2
to enable autoreload when you change the code
* tensorflow
* itchat
* opencv3
* scipy
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

## TODOs
* Add notification functionality
* Upload the corn.stanford.edu
* Add a separate thread, which could send messages on the computer
* Add Google search scraper
* Add image search scraper

## File System
utils.py: various utility methods
rules.json: hand-written text replies
computer\_vision.py: computer vision program which returns image label
natural\_language\_processing.py: nlp program which returns a reply given a text message
models: directory containing the tensorflow/models module
pre\_trained: directory which stores the model ckpt
data.json: json file containing all private data
