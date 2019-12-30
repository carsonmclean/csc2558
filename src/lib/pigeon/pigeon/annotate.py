import functools
import random
import time

import pandas as pd
from IPython.display import clear_output, display
from ipywidgets import Button, Dropdown, FloatSlider, HBox, HTML, IntSlider, Output, Textarea


def annotate(examples,
             options=None,
             shuffle=False,
             include_skip=True,
             display_fn=display,
             volunteer_name = None):
    """
    Build an interactive widget for annotating a list of input examples.

    Parameters
    ----------
    examples: list(any), list of items to annotate
    options: list(any) or tuple(start, end, [step]) or None
             if list: list of labels for binary classification task (Dropdown or Buttons)
             if tuple: range for regression task (IntSlider or FloatSlider)
             if None: arbitrary text input (TextArea)
    shuffle: bool, shuffle the examples before annotating
    include_skip: bool, include option to skip example while annotating
    display_fn: func, function for displaying an example to the user

    Returns
    -------
    annotations : list of tuples, list of annotated examples (example, label)
    """
    if shuffle:
        random.shuffle(examples)

    annotations = pd.DataFrame(columns=['filename', 'annotation'])
    current_index = -1
    start_time = end_time = time.time()

    def set_label_text():
        nonlocal count_label
        count_label.value = '{} examples annotated, {} examples left'.format(
            len(annotations), len(examples) - current_index
        )

    def show_next():
        nonlocal current_index
        current_index += 1
        set_label_text()
        if current_index >= len(examples):
            for btn in buttons:
                btn.disabled = True
            print('Annotation done.')
            return
        with out:
            clear_output(wait=True)
            display_fn(examples.iloc[current_index]['data'])
            nonlocal start_time
            start_time = time.time()

    def add_annotation(annotation):
        end_time = time.time()
        nonlocal start_time
        label_time = end_time - start_time
        nonlocal annotations
        annotations = annotations.append({'filename': examples.iloc[current_index]['filename'],
                                          'annotation': annotation,
                                          'time': label_time,
                                          'volunteer_name': volunteer_name.name},
                                         ignore_index=True)
        print(annotations)
        show_next()

    def skip(btn):
        show_next()

    count_label = HTML()
    set_label_text()
    display(count_label)

    if type(options) == list:
        task_type = 'classification'
    elif type(options) == tuple and len(options) in [2, 3]:
        task_type = 'regression'
    elif options is None:
        task_type = 'captioning'
    else:
        raise Exception('Invalid options')

    buttons = []
    
    if task_type == 'classification':
        use_dropdown = len(options) > 25

        if use_dropdown:
            dd = Dropdown(options=options)
            display(dd)
            btn = Button(description='submit')
            def on_click(btn):
                add_annotation(dd.value)
            btn.on_click(on_click)
            buttons.append(btn)
        
        else:
            for label in options:
                btn = Button(description=label)
                def on_click(label, btn):
                    add_annotation(label)
                btn.on_click(functools.partial(on_click, label))
                buttons.append(btn)

    elif task_type == 'regression':
        target_type = type(options[0])
        if target_type == int:
            cls = IntSlider
        else:
            cls = FloatSlider
        if len(options) == 2:
            min_val, max_val = options
            slider = cls(min=min_val, max=max_val)
        else:
            min_val, max_val, step_val = options
            slider = cls(min=min_val, max=max_val, step=step_val)
        display(slider)
        btn = Button(description='submit')
        def on_click(btn):
            add_annotation(slider.value)
        btn.on_click(on_click)
        buttons.append(btn)

    else:
        ta = Textarea()
        display(ta)
        btn = Button(description='submit')
        def on_click(btn):
            add_annotation(ta.value)
        btn.on_click(on_click)
        buttons.append(btn)

    if include_skip:
        btn = Button(description='skip')
        btn.on_click(skip)
        buttons.append(btn)

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst.

        Ned Batchelder
        https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
        """
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    # display buttons across multiple rows
    button_chunks = chunks(buttons, 5)
    for chunk in button_chunks:
        box = HBox(chunk)
        display(box)

    out = Output()
    display(out)

    show_next()

    return annotations
