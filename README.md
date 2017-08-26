Wechat robot for fun

Currently it works in a single group chat. Replace the trigger\_user set with a set of group chat ids you want to make it work.

The current text response is from tuling robot.

Working on image classification

## Prerequisites
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

## TODOs
* Add notification functionality
* Use mobilenet+ssd
* Make the code more efficient
