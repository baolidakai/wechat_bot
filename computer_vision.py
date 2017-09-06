# Computer vision code
import tensorflow as tf
import numpy as np
import cv2
import os

import sys
sys.path.append(os.path.join(os.getcwd(), 'models/slim'))

from datasets import imagenet
from nets import inception
from preprocessing import inception_preprocessing

from tensorflow.contrib import slim

print('Doing everything from scratch!')

labels = imagenet.create_readable_names_for_imagenet_labels()

image_size = inception.inception_v3.default_image_size
image_string = tf.placeholder(tf.string, name='img')
image = tf.image.decode_jpeg(image_string, channels=3)
processed_image = inception_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
processed_images = tf.expand_dims(processed_image, 0)

with slim.arg_scope(inception.inception_v3_arg_scope()):
  try:
    logits, _ = inception.inception_v3(processed_images, num_classes=1001, is_training=False, reuse=True)
  except:
    logits, _ = inception.inception_v3(processed_images, num_classes=1001, is_training=False, reuse=False)

probabilities = tf.nn.softmax(logits)

init_fn = slim.assign_from_checkpoint_fn('pre_trained/inception_v3.ckpt', slim.get_model_variables('InceptionV3'))

sess = tf.Session()
init_fn(sess)

# Convert the src image to dst image, and optionally return info about the image.
# Args:
#   src: the location of source image
#   dst: the location of destination image
# Returns:
#   info: optional, message about the source image
def convert_image(src, dst):
  print('Working on {}'.format(src))
  with open(src, 'rb') as image_file:
    img_string = image_file.read()
  np_image, np_probabilities = sess.run([image, probabilities], feed_dict={image_string: img_string})
  np_probabilities = np_probabilities[0, 0:]
  rtn = labels[np.argmax(np_probabilities)]
  return rtn
