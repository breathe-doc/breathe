Template
========

.. cpp:namespace:: @ex_template_first

Breathe has support for class and function templates. They are output as
follows. For a class with a single template parameter:

.. code-block:: rst

   .. doxygenclass:: templateclass
      :project: template_class
      :members:

It renders as:

----

.. doxygenclass:: templateclass
   :project: template_class
   :members:

----

.. cpp:namespace:: @ex_template_multiple

With multiple template parameters it renders as:

----

.. doxygenclass:: anothertemplateclass
   :project: template_class_non_type
   :members:

----

.. cpp:namespace:: @ex_template_function_single

A function with single template parameter renders as:

----

.. doxygenfunction:: function1
   :project: template_function

----

.. cpp:namespace:: @ex_template_function_single_specialization

If specialized for a given type it renders as:

----

.. doxygenfunction:: function1< std::string >
   :project: template_function

----

.. cpp:namespace:: @ex_template_function_multiple

With multiple template parameters it renders as:

----

.. doxygenfunction:: function2
   :project: template_function
