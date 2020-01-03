import pickle

import numpy as np
import pandas as pd
from IPython.display import display
from ipywidgets import Text

from lib.annotator import Annotator
from lib.example import Example
from lib.orderings import EpsilonRandom, Random, Same


def get_images():
    data = pd.read_pickle('./../../data/cifar-100/cifar-100.pkl')
    images = data[['filename','data', 'coarse_label_str']]
    return images.sample(100)

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
        self.get_volunteer_info()
        self.setup_annotator()


    def get_volunteer_info(self):
        name = Text(description='Name:', continuous_update=False)
        def update_volunteer_name(change):
            self.volunteer.name = name.value

        name.observe(update_volunteer_name)
        display(name)

    def setup_annotator(self):
        self.annotator.set_volunteer(self.volunteer)

        images = get_images()
        self.annotator.set_options(images['coarse_label_str'].unique().tolist())

        examples = []
        batch_i = 0
        n = 4
        orderings = [EpsilonRandom(images, n), Random(images, n), Same(images, n)]
        # for ordering in orderings:
        while len(orderings) > 0:
            batch_i += 1
            ordering = np.random.choice(orderings)
            batch = ordering.get_batch()
            if not type(batch) == pd.DataFrame and not batch:
                orderings.remove(ordering)
                continue

            for i, image in batch.iterrows():
                attrs = {'ordering': ordering.name,
                         'batch_i': batch_i}
                example = Example(image.filename, image['data'], image.coarse_label_str, attrs)
                examples.append(example)

        self.annotator.add_examples(examples)

        self.annotator.next()

