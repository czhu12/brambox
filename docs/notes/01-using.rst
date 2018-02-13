Using Brambox
=============
This toolbox contains both library packages and scripts.
After you installed brambox you can run the provided scripts from anywhere on the command line. |br|
The scripts that come with brambox are:

.. exec::
   import os
   scripts = os.listdir('../scripts')
   for s in scripts:
     print('  - %s' % s)

.. note::
   For more info about their usage, run the following command: |br|
   ``some_brambox_script.py --help``


Parsers
-------
The main purpose of brambox is to convert and analyse annotations and detections.
It has 2 functions :func:`~brambox.boxes.parse` and :func:`~brambox.boxes.generate` for reading or writing annotations and detections.
 
Some parsers require extra information upon initialisation. This information is passed to the parser through the keyword arguments.
To know which keyword arguments you need to pass to the :func:`~brambox.boxes.parse` and :func:`~brambox.boxes.generate` functions, take a look at the documentation for the specific parser you want to use.
Just pass on the parameters of the parser as keyword arguments: ``parameter_name = <value>``.

The output of the :func:`~brambox.boxes.parse` function is a dictionary.
The keys of the dictionary represent *image_identifiers* and their values are *lists of bounding boxes*.

>>> {
>>>   'image_001': [box, box, box, box],
>>>   'image_002': [box, box],
>>>   'image_003': [],
>>>   'image_004': [box, box, box, box, box, box],
>>>   ...
>>> }
 
.. rubric:: Example

>>> import brambox.boxes as bbb
>>> annotations = bbb.parse(bbb.annotation_formats['pickle'], 'path/to/pickle.pkl')
>>> bbb.generate(bbb.annotation_formats['yaml'], annotations, 'path/to/new/yaml.yml')

>>> # Darknet has one file per image and requires some special keyword arguments
>>> # We also use an identifier function here, to get unique image_identifiers
>>>
>>> import os
>>> import brambox.boxes as bbb
>>> 
>>> def identify_fn(filepath):
>>>   """ Generate a unique identifier from the path: file/to/path.txt -> file.to.path """
>>>   no_ext = os.path.splitext(filepath)[0]
>>>   return no_ext.replace('/', '.')
>>>
>>> annotations = bbb.parse('anno_darknet', 'multiple/*/files_*.txt', identify_fn, image_width=416, image_height=416, class_label_map=['cat', 'person', 'tree'])


Statistics
----------
Once your annotations and detections are read, you can perform a series of statistical computations on them.
Before computing your statistics, you can :ref:`filter <filters-label>` or :ref:`modify <modifiers-label>` your bounding boxes.

Modifying your bounding boxes, happens with the :func:`~brambox.boxes.util.modifiers.modify` function, and filtering with the :func:`~brambox.boxes.util.filters.filter_ignore` and :func:`~brambox.boxes.util.filters.filter_discard` functions. These functions take 2 parameters, a *dictionary with your bounding boxes per image* and a *list of filters/modifiers*. 

.. note::
   The :func:`~brambox.boxes.util.filters.filter_ignore` function only works with
   :class:`~brambox.boxes.annotations.Annotation` objects and will set their ``ignore`` flag to **True**.
   This flag will then get used in the statistical functions to ignore these annotations,
   together with the matching detection (if there is one). |br|
   :func:`~brambox.boxes.util.filters.filter_discard` works with any :class:`~brambox.boxes.box.Box` object
   and will simply remove them from the dictionary.

.. rubric:: Example

>>> import copy
>>> import brambox.boxes as bbb
>>>
>>> # Read annotations
>>> annotations = bbb.parse('anno_pickle', 'path/to/pickle.pkl')
>>> 
>>> # Remove all annotations without the class labels aeroplanes and boats
>>> bbb.filter_discard(annotations, [ bbb.ClassLabel_filter(['aeroplanes', 'boats']) ])
>>>
>>> # Mark difficult and occluded annotations as ignore
>>> bbb.filter_ignore(annotations, [
>>>   lambda anno: not anno.difficult,
>>>   lambda anno: not anno.occluded
>>> ])
>>>
>>> # Rescale the annotations (as an example, we copy the annotations in stead of modifying it)
>>> anno_rescaled = bbb.modify(copy.deepcopy(annotations), [ bbb.Scale_modifier(2) ])

Computing the actual statistics requires parsing annotations and detections,
and passing them to the right statistical function.
This function will usually output values that you can plot in a graph, using your favourite plotting tool.
Here are some examples, where we plot the values using matplotlib_.

.. rubric:: Example

>>> import matplotlib.pyplot as plt
>>> import brambox.boxes as bbb
>>>
>>> # Read annotations and detections
>>> annotations = bbb.parse('anno_pickle', 'path/to/annotation/pickle.pkl')
>>> detections = bbb.parse('det_pickle', 'path/to/detection/pickle.pkl')
>>>
>>> # Generate PR-curve and compute mAP
>>> plt.figure()
>>>
>>> p,r = bbb.pr(detections, annotations)
>>> ap = bbb.ap(p,r)
>>> plt.plot(r, p, label=f'mAP: {round(ap*100, 2)}%')
>>>
>>> plt.gcf().suptitle('PR-curve example')
>>> plt.gca().set_ylabel('Precision')
>>> plt.gca().set_xlabel('Recall')
>>> plt.gca().set_xlim([0, 1])
>>> plt.gca().set_ylim([0, 1])
>>> plt.show()

>>> import copy
>>> import matplotlib.pyplot as plt
>>> import brambox.boxes as bbb
>>>
>>> # Read annotations and detections
>>> annotations = bbb.parse('anno_pickle', 'path/to/annotation/pickle.pkl')
>>> detections = bbb.parse('det_pickle', 'path/to/detection/pickle.pkl')
>>>
>>> # Generate PR-curve and compute AP for every individual class.
>>> plt.figure()
>>>
>>> classes = ['aeroplane', 'boat', 'person', 'cat', 'dog']
>>> for c in classes:
>>>   anno_c = bbb.filter_discard(copy.deepcopy(annotations), [ lambda anno: anno.class_label == c ])
>>>   det_c  = bbb.filter_discard(copy.deepcopy(detections), [ lambda det: det.class_label == c ])
>>>   p,r = bbb.pr(det_c, anno_c)
>>>   ap = bbb.ap(p,r)
>>>   plt.plot(r, p, label=f'{c}: {round(ap*100, 2)}%')
>>>
>>> plt.gcf().suptitle('PR-curve individual example')
>>> plt.gca().set_ylabel('Precision')
>>> plt.gca().set_xlabel('Recall')
>>> plt.gca().set_xlim([0, 1])
>>> plt.gca().set_ylim([0, 1])
>>> plt.show()



.. include:: ../links.rst
