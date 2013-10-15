
.. _category-example:

doxygencategory Directive Example
=================================


Example without Members
-----------------------

This should work::

   .. doxygencategory:: NSObject(TestCategory)
      :project: category

It produces this output:

.. doxygencategory:: NSObject(TestCategory)
   :project: category
   :no-link:


Example with Members
--------------------

This should work::

   .. doxygencategory:: NSObject(TestCategory)
      :project: category
      :members:

It produces this output:

.. doxygencategory:: NSObject(TestCategory)
   :project: category
   :members:
   :no-link:


Working Example with Specific Members
-------------------------------------

This should work::

   .. doxygencategory:: NSObject(TestCategory)
      :project: category
      :members: testMethod:, testClassMethod:

It produces this output:

.. doxygencategory:: NSObject(TestCategory)
   :project: category
   :members: testInstanceMethod, testClassMethod
   :no-link:


Example as Outline
------------------

This should work::

   .. doxygencategory:: Nutshell
      :project: category
      :outline:
      :members:

It produces this output:

.. doxygencategory:: NSObject(TestCategory)
   :project: category
   :outline:
   :members:
   :no-link:


Failing Example
---------------

This intentionally fails::

   .. doxygencategory:: NSString(made_up_category)
      :project: category
      :members:

It produces the following warning message:

.. warning:: doxygencategory: Cannot find category "NSString(made_up_category)" in doxygen xml output


