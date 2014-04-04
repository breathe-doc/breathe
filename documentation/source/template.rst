Template
========

Breathe has support for class and function templates. They are output as
follows. For a class with a single template parameter::

   .. doxygenclass:: templateclass
      :project: template_class
      :members:

It renders as:

----

.. doxygenclass:: templateclass
   :project: template_class
   :members:

----

With multiple template parameters it renders as:

----

.. doxygenclass:: anothertemplateclass
   :project: template_class_non_type
   :members:

----

A function with single template parameter renders as:

----

.. doxygenfunction:: function1
   :project: template_function

----

With multiple template parameters it renders as:

----

.. doxygenfunction:: function2
   :project: template_function



