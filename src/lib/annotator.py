import time

import cv2
import pandas as pd
from IPython.display import Image, clear_output, display
from ipywidgets import Button, HBox, Layout, Output


class Annotator:

    def __init__(self):
        self.examples = []
        self.current_index = -1
        self.options = []
        self.buttons = []
        self.annotations = pd.DataFrame()
        self.annotations_path = '../../data/cifar-100'
        self.output = None
        self.start_time = None
        self.end_time = None
        self.volunteer = None

    def set_volunteer(self, volunteer):
        self.volunteer = volunteer

    def add_examples(self, new_examples):
        self.examples.extend(new_examples)

    def set_options(self, new_options, update=True):
        self.options = sorted(new_options)
        if update:
            self.setup_buttons()

    def setup_buttons(self):
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst.

            Ned Batchelder
            https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
            """
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        for label in self.options:
            btn = Button(description=label,
                         layout=Layout(width='220px',
                                       height='40px'))
            btn.style.font_weight = 'bolder'
            def on_click(btn):
                self.end_time = time.time()
                self.add_annotation(btn.description)

            btn.on_click(on_click)
            self.buttons.append(btn)

        # display buttons across multiple rows
        button_chunks = chunks(self.buttons, 5)
        for chunk in button_chunks:
            box = HBox(chunk,
                       layout=Layout(margin='-10px 0px'))
            display(box)


    def add_annotation(self, annotation):

        if self.current_index >= len(self.examples):
            return

        record = {
            'id': self.examples[self.current_index].id,
            'truth': self.examples[self.current_index].truth,
            'annotation': annotation,
            'time': self.end_time - self.start_time,
            'volunteer': self.volunteer.name,
            'ts': time.time()
        }
        record.update(self.examples[self.current_index].attrs)
        # print(record)
        self.annotations = self.annotations.append(record,
                                                   ignore_index=True)

        self.annotations.to_csv(f'{self.annotations_path}/annotations.csv')
        # print(self.annotations)

        self.next()

    def display_fn(self, img):
        # ctmakro
        # https://gist.github.com/ctmakro/3ae3cd9538390b706820cd01dac6861f
        _, ret = cv2.imencode('.jpg', img)
        i = Image(data=ret,
                  width=150)
        display(i)

    def next(self):
        self.current_index += 1
        if self.current_index >= len(self.examples):
            print('Annotations complete!')
            return

        if not self.output:  # need to initialize Output/display() here vs init else image in top notebook cell
            self.setup_display()

        with self.output:
            clear_output(wait=True)
            self.display_fn(self.examples[self.current_index].data)
            self.start_time = time.time()

    def setup_display(self):
        self.output = Output()
        display(self.output)
