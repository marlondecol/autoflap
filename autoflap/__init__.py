#!/usr/bin/env python
"""
AutoFLAP
========

The AutoFLAP offers functionality to create design files for Finite
State Machines (FSM), also called Finite State Automata, for the JFLAP
software.

Through this package it is possible to build automata in several ways,
the most common one being the import of their representation
spreadsheets (i.e. CSV files). But it can also be done using the classes
and methods provided by the API, which allow the handling of their
states, transitions and other attributes in an objective way. Regardless
of the chosen way, after the completion of all the relevant procedures
for the automata, the tool exports each automaton in a JFLAP design
file, with the respective states pleasantly positioned.

This package has classes for automata, states and transitions. It also
has a module with several classes of customized exceptions for the
occurrence of specific AutoFLAP errors. Some constants are also
available with the default values ​​for some characteristics.

AutoFLAP CLI
------------

In addition to the features available by the package itself, that is,
the AutoFLAP API, this software also has a Command Line Interface (CLI),
which performs the export of JFLAP design files from the import of
automaton representation spreadsheets, with several options
configuration using command line arguments.

To use the AutoFLAP CLI, just run the `autoflap` library module using
the Python `-m` option in a terminal, followed by the appropriate
arguments, as shown below.

  $ python -m autoflap [-h] [-v] [-i <symbol>] [-f <symbol>]
                       [-n <symbol>] [-e <symbol>] [-s <index>]
                       [-y <index>] [-r <factor>] [-m <margin>] [-q]
                       [-o [<path>]]
                       <csv_file> [<csv_file> ...]

It is mandatory to enter the paths of the input CSV files from which the
automata for JFLAP will be generated. Other arguments are optional, and
more details about them are available using the `-h` or `--help`
argument when executing the command.

Automaton Representation Spreadsheet
------------------------------------

The automaton representation spreadsheet is a table containing the
expected transitions for each of its states, according to the conditions
to which they are submitted.

It usually has the alphabet accepted by the automaton arranged in its
header (i.e. the first line), the states in the second column and the
indications of the initial and final states in the first column.

The following is an example of an automaton representation spreadsheet.

  ,,a,b,c,-
  >,q1,q2,-,q1,q3
  ,q2,q2,q1,q3,-
  *,q3,-,q1,q3,q2

The dash in the header is an indication of the empty character,
represented, in JFLAP, by the lowercase Greek letters epsilon or lambda.
The dashes in the rest of the cells, on the other hand, indicate the
absence of transition from the respective states given the respective
characters.

In this example, the angle bracket and the asterisk indicate,
respectively, that the state `q1` is the initial state and that the
state `q3` is the final state. It is worth mentioning that a single
state can be valid for both.

These settings, in addition to others, can be easily changed while using
the package, as needed.

Common Usage
------------

The following is an example of common usage of the package.

  1. First, you must import the package and create an instance of the
  `Automaton` class.

  >>> import autoflap as af
  >>> automaton = af.Automaton()

  2. After defining the path of the input CSV file (the variable
  `csv_file` below), it is imported and then the automaton is exported
  to a JFLAP design file.

  >>> automaton.parse_csv(csv_file)
  >>> automaton.build_jff(csv_file)

Of course, it is possible to define other parameters for the execution
of these methods, as needed. For this, it is recommended to consult the
documentation in the `Automaton` class for each one of them.
"""
__version__ = '1.0.0'

# Main application modules.
from .automaton.automaton import *
from .automaton.state import *
from .automaton.transition import *

# Custom exception classes.
from .automaton.error import *

# Default values and constants.
from .constants import *
