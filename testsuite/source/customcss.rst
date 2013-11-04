
.. highlight:: css

Custom CSS
==========

In order to help with the output styling in HTML, Breathe attaches some custom
classes to parts of the document. There are three such classes:

**breatheparameterlist**
   Used to keep the description of a parameter displayed inline with the
   parameter name. The Breathe docs use::

      .breatheparameterlist li tt + p {
              display: inline;
      }

**breatheenumvalues**
   Used to keep the description of an enum displayed inline with the
   enum name. The Breathe docs use::

      .breatheenumvalues li tt + p {
              display: inline;
      }

