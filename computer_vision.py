# Computer vision code
# import cv2
import tensorflow as tf
import numpy as np
import os

from tensorflow.contrib import slim

from models.slim.datasets import imagenet
from model.slim.nets import inception
from model.slim.preprocessing import inception_preprocessing

# Convert the src image to dst image, and optionally return info about the image.
# Args:
#   src: the location of source image
#   dst: the location of destination image
# Returns:
#   info: optional, message about the source image
def convert_image(src, dst):
  return 'I can see the image.'


