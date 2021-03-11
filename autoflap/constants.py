"""
AutoFLAP Constants
==================

Definitions of the constants made available to the entire application.

These constants define some attributes of the application as a whole,
mainly those related to the JFLAP automaton designs.
"""
__all__ = [
    'DEFAULT_EMPTY_STRING_SYMBOL', 'DEFAULT_FINAL_STATE_SYMBOL',
    'DEFAULT_INITIAL_STATE_SYMBOL', 'DEFAULT_NO_TRANSITION_SYMBOL',
    'DEFAULT_STATE_SYMBOLS_COL', 'DEFAULT_STATES_COL',
    'DEFAULT_DRAWING_MARGIN', 'DEFAULT_DRAWING_RADIUS_FACTOR',
    'DEFAULT_OUTPUT_DIR', 'JFLAP_FILE_EXTENSION'
]

from numbers import Integral, Real
from typing import Text

# Default symbols for states and transitions.
DEFAULT_EMPTY_STRING_SYMBOL: Text = '-'
DEFAULT_FINAL_STATE_SYMBOL: Text = '*'
DEFAULT_INITIAL_STATE_SYMBOL: Text = '>'
DEFAULT_NO_TRANSITION_SYMBOL: Text = '-'

# Default indices for states and state symbols columns.
DEFAULT_STATE_SYMBOLS_COL: Integral = 0
DEFAULT_STATES_COL: Integral = 1

# Default values for states positioning.
DEFAULT_DRAWING_MARGIN: Real = 100
DEFAULT_DRAWING_RADIUS_FACTOR: Real = 25

# The input file directory is the default output directory.
DEFAULT_OUTPUT_DIR: Text = '.'

# The JFLAP design file extension.
JFLAP_FILE_EXTENSION: Text = '.jff'
