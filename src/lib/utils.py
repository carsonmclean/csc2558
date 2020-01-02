import pickle

import pandas as pd
from IPython.display import display
from ipywidgets import Text

from lib.annotator import Annotator
from lib.example import Example


def get_images():
    data = pd.read_pickle('./../../data/cifar-100/cifar-100.pkl')
    images = data[['filename','data', 'coarse_label_str']]
    return images.iloc[:100]


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


class Experiment:
    volunteer = Volunteer()
    annotator = Annotator()

    def run(self):
        print('running experiment')

        self.get_volunteer_info()
        self.setup_annotator()


    def get_volunteer_info(self):
        name = Text(description='Name:', continuous_update=False)
        def update_volunteer_name(change):
            self.volunteer.name = name.value

        name.observe(update_volunteer_name)
        display(name)

    def setup_annotator(self):
        labels = get_labels()
        self.annotator.set_options(labels)
        images = get_images()
        examples = []
        for i, image in images.iterrows():
            example = Example(image.filename, image['data'], image.coarse_label_str)
            examples.append(example)
        self.annotator.add_examples(examples)
        self.annotator.next()

