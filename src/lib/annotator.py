from IPython.display import display
from ipywidgets import Button, HBox


class Annotator:
    examples = []
    options = []
    buttons = []

    def __init__(self):
        pass

    def add_examples(self, new_examples):
        self.examples.append(new_examples)

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
                print(f'{btn.description}')

            btn.on_click(on_click)
            self.buttons.append(btn)
        # display buttons across multiple rows
        button_chunks = chunks(self.buttons, 5)
        for chunk in button_chunks:
            box = HBox(chunk)
            display(box)

    def add_annotation(self, annotation):
        pass