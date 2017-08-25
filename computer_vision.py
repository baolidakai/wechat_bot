# Computer vision code
# import cv2
import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt
import base64

import urllib.request as urllib

import sys
sys.path.append(r'/home/radmin/programs/wechat/models/slim') # Change this on your computer

from datasets import imagenet
from nets import inception
from preprocessing import inception_preprocessing

from tensorflow.contrib import slim

# Convert the src image to dst image, and optionally return info about the image.
# Args:
#   src: the location of source image
#   dst: the location of destination image
# Returns:
#   info: optional, message about the source image
def convert_image(src, dst):
  print('Working on {}'.format(src))
  image_size = inception.inception_v3.default_image_size
  with tf.Graph().as_default():
    with open(src, 'rb') as image_file:
      image_string = image_file.read()

    image = tf.image.decode_jpeg(image_string, channels=3)
    processed_image = inception_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
    processed_images  = tf.expand_dims(processed_image, 0)

    with slim.arg_scope(inception.inception_v3_arg_scope()):
      logits, _ = inception.inception_v3(processed_images, num_classes=1001, is_training=False)

    probabilities = tf.nn.softmax(logits)

    init_fn = slim.assign_from_checkpoint_fn('pre_trained/inception_v3.ckpt', slim.get_model_variables('InceptionV3'))

    with tf.Session() as sess:
      init_fn(sess)
      np_image, probabilities = sess.run([image, probabilities])
      probabilities = probabilities[0, 0:]
      sorted_inds = [i[0] for i in sorted(enumerate(-probabilities), key=lambda x: x[1])]

    names = imagenet.create_readable_names_for_imagenet_labels()
    rtn = 'Probability %0.2f%% => [%s]' % (probabilities[sorted_inds[0]] * 100, names[sorted_inds[0]])
  print('Got the result')
  print(rtn)
  return rtn
