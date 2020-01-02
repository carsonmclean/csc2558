import time

import cv2
import pandas as pd
from IPython.display import Image, clear_output, display
from ipywidgets import Button, HBox, Output


class Annotator:

    def __init__(self):
        self.examples = []
        self.current_index = -1
        self.options = []
        self.buttons = []
        self.annotations = pd.DataFrame()
        self.output = None

    def add_examples(self, new_examples):
        self.examples.extend(new_examples)

    def set_options(self, new_options, update=True):
        self.options = new_options
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
            btn = Button(description=label)

            def on_click(btn):
                self.add_annotation(btn.description)

            btn.on_click(on_click)
            self.buttons.append(btn)

        # display buttons across multiple rows
        button_chunks = chunks(self.buttons, 5)
        for chunk in button_chunks:
            box = HBox(chunk)
            display(box)

    def add_annotation(self, annotation):
        self.annotations = self.annotations.append({
                'id': 'TODO',
                'annotation': annotation,
                'ts': time.time()
            },
            ignore_index=True)

        self.next()

    def display_fn(self, img):
        # ctmakro
        # https://gist.github.com/ctmakro/3ae3cd9538390b706820cd01dac6861f
        _, ret = cv2.imencode('.jpg', img)
        i = Image(data=ret)
        display(i)

    def next(self):
        self.current_index += 1
        if self.current_index >= len(self.examples):
            print('Annotations complete!')

        if not self.output:  # need to initialize Output/display() here vs init else image in top notebook cell
            self.setup_display()

        with self.output:
            clear_output(wait=True)
            self.display_fn(self.examples[self.current_index].data)

    def setup_display(self):
        self.output = Output()
        display(self.output)