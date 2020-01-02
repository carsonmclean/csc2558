import numpy as np


class Random:
    name = 'random'

    def __init__(self, examples, n):
        self.examples = examples
        self.n = n

    def get_batch(self):
        samples = self.examples.sample(self.n)
        self.examples.drop(samples.index, inplace=True)  # use inplace or else original DF unchanged in Experiment()

        return samples


class Same:
    name = 'same'

    def __init__(self, examples, n):
        self.examples = examples
        self.n = n

    def get_batch(self):
        label = np.random.choice(self.examples['coarse_label_str'].unique())
        samples = self.examples[self.examples['coarse_label_str'] == label].sample(self.n)
        self.examples.drop(samples.index, inplace=True)

        return samples