import pickle

import cv2
import pandas as pd
from IPython.display import Image, display
from ipywidgets import Text

import lib.pigeon.pigeon as pigeon
from lib.annotator import Annotator


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


class Volunteer:
    name = None

class Treatment:
    name = None

class Experiment:
    volunteer = Volunteer()
    annotator = Annotator()

    def run(self):
        print('running experiment')

        self.get_volunteer_info()
        self.setup_annotator()

        self.run_training()
        # self.run_experiment()

    def get_volunteer_info(self):
        name = Text(description='Name:', continuous_update=False)
        def update_volunteer_name(change):
            self.volunteer.name = name.value

        name.observe(update_volunteer_name)
        display(name)

    def setup_annotator(self):
        self.annotator.set_options(get_labels())

    def run_training(self):
        pass

    def run_experiment(self):
        # run all sub-experiments once
        annotations = pigeon.annotate(examples=get_images(),
                                      options=get_labels(),
                                      shuffle=False,
                                      include_skip=True,
                                      display_fn=display_fn,
                                      volunteer_name=self.volunteer)

        # run sub-experiments until quit or end of examples

        pass
