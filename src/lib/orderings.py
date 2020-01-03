import numpy as np


class Random:
    name = 'random'

    def __init__(self, examples, n):
        self.examples = examples
        self.n = n

    def get_batch(self):
        try:
            samples = self.examples.sample(self.n)
        except ValueError:
            return None

        self.examples.drop(samples.index, inplace=True)  # use inplace or else original DF unchanged in Experiment()

        return samples


class Same:
    name = 'same'

    def __init__(self, examples, n):
        self.examples = examples
        self.n = n

    def get_batch(self):
        label = np.random.choice(self.examples['coarse_label_str'].unique())
        try:
            samples = self.examples[self.examples['coarse_label_str'] == label].sample(self.n)
        except ValueError:
            return None

        self.examples.drop(samples.index, inplace=True)

        return samples


class EpsilonRandom:
    name = 'epsilon_random'

    def __init__(self, examples, n, epsilon=0.75):
        self.examples = examples
        self.n = n
        self.epsilon = epsilon

    def get_batch(self):
        label = np.random.choice(self.examples['coarse_label_str'].unique())
        n_labels = int(self.epsilon * self.n)
        try:
            samples_label = self.examples[self.examples['coarse_label_str'] == label].sample(n_labels)
            samples_non_label = self.examples[self.examples['coarse_label_str'] != label].sample(self.n - n_labels)
        except ValueError:
            return None

        combined = samples_label.append(samples_non_label).sample(frac=1)  # sample 100% to shuffle
        self.examples.drop(combined.index, inplace=True)

        return combined
