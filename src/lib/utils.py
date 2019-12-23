import pickle

import cv2
import pandas as pd
from IPython.display import Image, display


def display_fn(img):
    # ctmakro
    # https://gist.github.com/ctmakro/3ae3cd9538390b706820cd01dac6861f
    _, ret = cv2.imencode('.jpg', img)
    i = Image(data=ret)
    display(i)


def get_images():
    data = pd.read_pickle('./../../data/cifar-100/cifar-100.pkl')
    images = data[['filename','data']]
    return images


def get_labels():
    data = pd.read_pickle('./../../data/cifar-100/cifar-100.pkl')
    # fine_labels = data['fine_label_str'].unique().tolist()
    coarse_labels = data['coarse_label_str'].unique().tolist()

    return coarse_labels


def unpickle(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict