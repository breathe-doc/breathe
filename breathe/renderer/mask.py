"""
Masks
=====

Masks are related to filters. Filters can block the processing of particular parts of the xml
hierarchy but they can only work on node level. If the part of the xml hierarchy that you want to
filter out is read in as an instance of one of the classes in parser/doxygen/*.py then you can use
the filters. However, if you want to filter out an attribute from one of the nodes (and some of the
xml child nodes are read in as attributes on their parents) then you can't use a filter.

We introduce the Mask's to fulfil this need. The masks are designed to be applied to a particular
node type and to limit the access to particular attributes on the node. For example, then
NoParameterNamesMask wraps a node a returns all its standard attributes but returns None for the
'declname' and 'defname' attributes.

Currently the Mask functionality is only used for the text signature rendering for doing function
matching.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from breathe import parser

if TYPE_CHECKING:
    from typing import Callable


def no_parameter_names(node: parser.NodeOrValue) -> parser.Node_paramType:
    assert isinstance(node, parser.Node_paramType)
    return parser.Node_paramType(
        array=node.array,
        attributes=node.attributes,
        briefdescription=node.briefdescription,
        declname=None,
        defname=None,
        defval=None,
        type=node.type,
        typeconstraint=node.typeconstraint,
    )


class MaskFactoryBase:
    def mask(self, data_object):
        raise NotImplementedError


class MaskFactory(MaskFactoryBase):
    def __init__(
        self,
        lookup: dict[type[parser.NodeOrValue], Callable[[parser.NodeOrValue], parser.NodeOrValue]],
    ):
        self.lookup = lookup

    def mask(self, data_object: parser.NodeOrValue) -> parser.NodeOrValue:
        m = self.lookup.get(type(data_object))
        if m is None:
            return data_object
        return m(data_object)


class NullMaskFactory(MaskFactoryBase):
    def mask(self, data_object: parser.NodeOrValue) -> parser.NodeOrValue:
        return data_object
