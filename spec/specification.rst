
Breathe Specification
=====================

Nodes
-----

The planned nodes are::

   doxygen_node

This node should accept a path to a set of doxygen xml output and the name and
type of a doxygen "item" to document. These will be provided by the config file,
the directive and the directive's arguments respectively.

It will also be possible to override the xml output path as a directive option
to account for different sets of doxygen output being used.

Directives
----------

The planned directives are::

   doxygenclass
   doxygenfunction

Roles
-----

No restructured text roles are planned.

