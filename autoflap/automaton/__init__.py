"""
AutoFLAP Automaton Modules
==========================

This subpackage provides the classes and resources necessary for the
generation of automata and the subsequent export of JFLAP design files.

It is not necessary to import this subpackage or any of its modules
individually, since the `autoflap` package already does this implicitly.
"""
# Main application classes.
from .automaton import *
from .state import *
from .transition import *

# Custom exception classes.
from .error import *
