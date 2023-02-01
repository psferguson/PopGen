#!/usr/bin/env python
"""
Factory for generating instances of classes
"""
import sys
from collections import OrderedDict as odict #FIXME: are all dicts now ordered dicts
import inspect


def factory(type, module=None, **kwargs):
    """
    Factory for creating objects. Arguments are passed directly to the
    constructor of the chosen class.
    """
    cls = type
    if module is None: module = __name__
    fn = lambda member: inspect.isclass(member) and member.__module__==module
    classes = odict(inspect.getmembers(sys.modules[module], fn))
    members = odict([(k.lower(),v) for k,v in classes.items()])
    lower = cls.lower()
    if lower not in list(members.keys()):
        msg = "Unrecognized class: %s.%s"%(module,cls)
        raise KeyError(msg)
    return members[lower](**kwargs)

def isochroneFactory(name, **kwargs):
    module ="popgen"
    # First try this module
    try:    return factory(name, module=__name__, **kwargs)
    except KeyError: pass
    try:    return factory(name, module=module+'.composite', **kwargs)
    except KeyError: pass
    # Then try parsec
    try:    return factory(name, module=module+'.parsec', **kwargs)
    except KeyError: pass
    # Then try mesa
    try:    return factory(name, module=module+'.mesa', **kwargs)
    except KeyError: pass
    # Then try desd
    try:    return factory(name, module=module+'.dartmouth', **kwargs)
    except KeyError: pass

    raise KeyError('Unrecognized class: %s'%name)