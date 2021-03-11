"""
Finite State Automaton
======================

A finite state machine (FSM), or finite state automaton, is a
computational model of algorithms and logical sequences, such as regular
expression validation.

An automaton is made up of certain quantities of states and transitions,
which vary according to the application whose automaton represents.
"""
from __future__ import annotations

__all__ = ['Automaton']

import csv
import errno
import math
import os
from numbers import Integral, Real
from typing import List, Optional, Text
from xml.etree import ElementTree as ET

import autoflap as app
from . import error as err
from .. import constants as c
from .state import State
from .transition import Transition


class Automaton:
    """
    Provide functionality to create and manipulate a finite state
    automaton compatible with the JFLAP software.

    From this class it is possible to create an automaton in two ways.
    The first is through methods made available by this class for adding
    states and transitions, among other definitions. The second is by
    importing and parsing an automaton representation spreadsheet (i.e.
    a CSV file).

    After the automaton is completely defined, it is possible to export
    it to a JFLAP design file for proper use.

    A common use case is to execute, after instantiating an object of
    this class, first the `parse_csv` method, to read the states and
    transitions from the spreadsheet, and then the `build_jff` method,
    to export the automaton. There is also the possibility of handling
    states and transitions between the execution of these two methods,
    if necessary.
    """
    def __init__(self) -> None:
        """Instantiate a brand new automaton."""
        self.reset()

    def add_state(self, name: Text) -> State:
        """
        Create a new state with a given name and add it to this
        automaton.

        Parameters
        ----------
        name : Text
            The name of the new state.

        Returns
        -------
        State
            The instance of the new state.

        Raises
        ------
        StateExistsError
            There is already a state with this name.
        """
        if self.has_state(name):
            raise err.StateExistsError(name)

        state = State(name)

        self.__states.append(state)

        return state

    def add_transition(self,
                       origin: State,
                       target: Optional[State] = None,
                       when: Optional[Text] = None) -> Transition:
        """
        Instantiate a transition between two states or a state itself,
        with a given condition, and add it to this automaton.

        Parameters
        ----------
        origin : State
            The instance of the origin state, which must be part of this
            automaton.
        target : Optional[State], optional
            The instance of the target state, which must also be part of
            this automaton. If it is `None`, then it will be the origin
            state itself. Defaults to `None`.
        when : Optional[Text], optional
            A condition string for the transition, to define when it
            should be activated, or `None` if it is empty. Defaults to
            `None`.

        Returns
        -------
        Transition
            The instance of the new transition.

        Raises
        ------
        TransitionExistsError
            A transition with this origin and this condition already
            exists.
        StateNotFoundError
            The states of origin or target do not belong to this
            automaton.
        """
        if self.has_transition(origin, when):
            raise err.TransitionExistsError(origin.name, when)

        transition = Transition(origin, target, when)

        try:
            if not self.has_state(origin.name):
                raise err.StateNotFoundError(origin.name)

            if target is not None and not self.has_state(target.name):
                raise err.StateNotFoundError(target.name)
        except Exception as e:
            del transition

            raise e

        self.__transitions.append(transition)

        return transition

    def build_jff(
            self,
            filename: Text,
            dirname: Optional[Text] = c.DEFAULT_OUTPUT_DIR,
            drawing_radius_factor: Real = c.DEFAULT_DRAWING_RADIUS_FACTOR,
            drawing_margin: Real = c.DEFAULT_DRAWING_MARGIN) -> Text:
        """
        Build the JFLAP design of this automaton, which content is based
        on the XML format, and write it in a JFLAP design file.

        Parameters
        ----------
        filename : Text
            The name of the output file.
        dirname : Optional[Text], optional
            The directory where the output file must be written. If
            `None`, then the directory of `filename` will be used.
            Defaults to `DEFAULT_OUTPUT_DIR`.
        drawing_radius_factor : Real, optional
            Circle radius factor when designating the states positions.
            The radius is equal to this factor times the number of
            states of this automaton. Defaults to
            `DEFAULT_DRAWING_RADIUS_FACTOR`.
        drawing_margin : Real, optional
            Distance from the left and top margins from which the states
            must be positioned, in pixels. Defaults to
            `DEFAULT_DRAWING_MARGIN`.

        Returns
        -------
        Text
            The path for the output file.

        Raises
        ------
        NoInitialStateError
            An initial state was not defined.
        NoFinalStateError
            At least one final state must be defined.
        NotADirectoryError
            The output directory does not exist or is not a directory.
        FileExistsError
            A file with the same name already exists.
        """
        if not self.has_initial_state:
            raise err.NoInitialStateError()

        if not self.has_final_state:
            raise err.NoFinalStateError()

        filename = os.path.abspath(str(filename))

        output_file = filename if dirname is None else os.path.abspath(
            os.path.join(str(dirname),
                         os.path.split(filename)[-1]))

        dirname, filename = os.path.split(output_file)

        if not os.path.isdir(dirname):
            raise NotADirectoryError(errno.ENOTDIR, os.strerror(errno.ENOTDIR),
                                     dirname)

        if not filename.endswith(c.JFLAP_FILE_EXTENSION):
            output_file += c.JFLAP_FILE_EXTENSION

        if os.path.isfile(output_file):
            raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST),
                                  output_file)

        jff_comment = ET.Comment(f'Created with AutoFLAP {app.__version__}')

        jff_structure = ET.Element('structure')

        ET.SubElement(jff_structure, 'type').text = 'fa'

        jff_automaton = ET.SubElement(jff_structure, 'automaton')
        jff_automaton.append(ET.Comment('The list of states'))

        n = len(self.__states)

        for idx, state in enumerate(self.__states):
            jff_state = ET.SubElement(jff_automaton, 'state')
            jff_state.attrib = dict(id=str(idx), name=state.name)

            a = 2 * math.pi * idx / n + math.pi
            r = n * drawing_radius_factor

            position = lambda f: f'{r * f(a) + r + drawing_margin:.1f}'

            ET.SubElement(jff_state, 'x').text = position(math.cos)
            ET.SubElement(jff_state, 'y').text = position(math.sin)

            if self.initial_state == state:
                jff_state.append(ET.Element('initial'))

            if state.is_final:
                jff_state.append(ET.Element('final'))

        jff_automaton.append(ET.Comment('The list of transitions'))

        for transition in self.__transitions:
            jff_transition = ET.SubElement(jff_automaton, 'transition')

            ET.SubElement(jff_transition, 'from').text = str(
                self.__states.index(transition.origin))

            ET.SubElement(jff_transition, 'to').text = str(
                self.__states.index(transition.target))

            ET.SubElement(jff_transition, 'read').text = transition.when

        ET.indent(jff_structure, '\t')

        def tostring(xml: ET.Element, **kwargs) -> Text:
            return ET.tostring(xml, 'utf-8', **kwargs).decode('utf-8')

        jff = tostring(jff_structure, xml_declaration=True).splitlines()
        jff.insert(1, tostring(jff_comment))

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(jff))

        return output_file

    @property
    def final_states(self) -> List[State]:
        """
        List all the final states of this automaton.

        Returns
        -------
        List[State]
            A list containing the instances of all the final states of
            this automaton.
        """
        return [state for state in self.__states if state.is_final]

    def get_state(self, name: Text) -> Optional[State]:
        """
        Search for a state with a given name and return its instance, or
        `None` if not found.

        Parameters
        ----------
        name : Text
            The name of the state to be searched.

        Returns
        -------
        Optional[State]
            The instance of the state found, or `None` otherwise.
        """
        for state in self.__states:
            if state.name == name:
                return state

    def get_transition(self, origin: State,
                       when: Optional[Text]) -> Optional[Transition]:
        """
        Search for a transition with a given origin and condition and
        return its instance, or `None` if not found.

        Parameters
        ----------
        origin : State
            The instance of the origin state of the transition to be
            searched.
        when : Optional[Text]
            The condition string of the transition to be searched, or
            `None` if it is empty.

        Returns
        -------
        Optional[Transition]
            The instance of the transition found, or `None` otherwise.
        """
        for transition in self.__transitions:
            if transition.origin == origin and transition.when == when:
                return transition

    @property
    def has_final_state(self) -> bool:
        """
        Check whether this automaton has at least one final state.

        Returns
        -------
        bool
            `True` if this automaton has at least one final state,
            `False` otherwise.
        """
        return len(self.final_states) > 0

    @property
    def has_initial_state(self) -> bool:
        """
        Check whether this automaton has an initial state.

        Returns
        -------
        bool
            `True` if this automaton has an initial state, `False`
            otherwise.
        """
        return self.initial_state is not None

    def has_state(self, name: Text) -> bool:
        """
        Check whether this automaton has a state with a given name.

        Parameters
        ----------
        name : Text
            The name of the state to check.

        Returns
        -------
        bool
            `True` if this automaton has a state with the given name,
            `False` otherwise.
        """
        return self.get_state(name) is not None

    def has_transition(self, origin: State, when: Optional[Text]) -> bool:
        """
        Check whether this automaton has a transition with a given
        origin and condition.

        Parameters
        ----------
        origin : State
            The instance of the origin state of the transition to check.
        when : Optional[Text]
            The condition string of the transition to check, or `None`
            if it is empty.

        Returns
        -------
        bool
            `True` if this automaton has a transition with the given
            origin and condition, `False` otherwise.
        """
        return self.get_transition(origin, when) is not None

    @property
    def initial_state(self) -> Optional[State]:
        """
        Return the instance of the initial state of this automaton, if
        defined.

        Returns
        -------
        Optional[State]
            The instance of the initial state of this automaton, or
            `None` if it is not defined.
        """
        return self.__initial_state

    @initial_state.setter
    def initial_state(self, state: State) -> None:
        """
        Set a state of this automaton as its initial state.

        Parameters
        ----------
        state : State
            The state instance to be defined as initial.

        Raises
        ------
        TypeError
            Not a state instance.
        StateNotFoundError
            The state does not belong to this automaton.
        """
        if not isinstance(state, State):
            raise TypeError('not a state instance')

        if not self.has_state(state.name):
            raise err.StateNotFoundError(state.name)

        self.__initial_state = state

    def parse_csv(
        self,
        input_file: Text,
        initial_state_symbol: Text = c.DEFAULT_INITIAL_STATE_SYMBOL,
        final_state_symbol: Text = c.DEFAULT_FINAL_STATE_SYMBOL,
        no_transition_symbol: Text = c.DEFAULT_NO_TRANSITION_SYMBOL,
        empty_string_symbol: Text = c.DEFAULT_EMPTY_STRING_SYMBOL,
        states_col_index: Integral = c.DEFAULT_STATES_COL,
        state_symbols_col_index: Integral = c.DEFAULT_STATE_SYMBOLS_COL
    ) -> Automaton:
        """
        Read an input CSV file from an automaton representation
        spreadsheet and parse its states and transitions for this
        automaton instance.

        The CSV dialect of the file will be automatically interpreted
        during its reading.

        After the process is successfully completed, the instance of
        this automaton is returned.

        Parameters
        ----------
        input_file : Text
            The path to the input CSV file.
        initial_state_symbol : Text, optional
            The initial state symbol in spreadsheet, which is usually a
            single character. Defaults to
            `DEFAULT_INITIAL_STATE_SYMBOL`.
        final_state_symbol : Text, optional
            The final state symbol in spreadsheet, which is also usually
            a single character. Defaults to
            `DEFAULT_FINAL_STATE_SYMBOL`.
        no_transition_symbol : Text, optional
            The no transition symbol in spreadsheet, which, again, is
            also usually a single character. Defaults to
            `DEFAULT_NO_TRANSITION_SYMBOL`.
        empty_string_symbol : Text, optional
            The empty string representation symbol in spreadsheet,
            usually represented by the characters epsilon or lambda in
            JFLAP. Defaults to `DEFAULT_EMPTY_STRING_SYMBOL`.
        states_col_index : Integral, optional
            The states column index in spreadsheet. Defaults to
            `DEFAULT_STATES_COL`.
        state_symbols_col_index : Integral, optional
            The state symbols column index in spreadsheet. Defaults to
            `DEFAULT_STATE_SYMBOLS_COL`.

        Returns
        -------
        Automaton
            The instance of this automaton itself.

        Raises
        ------
        IndexError
            The index of the states column is the same as the index of
            the state symbols column.
        HeadersNotFoundError
            The spreadsheet headers (i.e. the column labels) were not
            found.
        InitialStateAlreadyDefinedError
            There was a second attempt to set the initial state. The
            initial state was already defined.
        StateNotFoundError
            The target state was not found in this automaton when
            defining a transition.
        """
        if states_col_index == state_symbols_col_index:
            raise IndexError('the state column index cannot be the same as ' \
                             'the state symbol column')

        input_file = os.path.abspath(input_file)

        with open(input_file, newline='') as file:
            dialect = csv.Sniffer().sniff(file.read(1024))

            file.seek(0)

            csv_file = csv.reader(file, dialect)

            try:
                next(csv_file)
            except StopIteration:
                raise err.HeadersNotFoundError()

            self.reset()

            try:
                for row in csv_file:
                    state = self.add_state(row.pop(states_col_index))

                    state_type = row.pop(state_symbols_col_index - (
                        state_symbols_col_index > states_col_index))

                    if initial_state_symbol in state_type:
                        if self.has_initial_state:
                            raise err.InitialStateAlreadyDefinedError(
                                self.initial_state.name)

                        self.initial_state = state

                    if final_state_symbol in state_type:
                        state.is_final = True

                file.seek(0)

                columns = next(csv_file)

                indices = sorted([states_col_index, state_symbols_col_index])
                indices.reverse()

                for i in indices:
                    columns.pop(i)

                for state in self.__states:
                    row = next(csv_file)

                    for i in indices:
                        row.pop(i)

                    for when, name in zip(columns, row):
                        if name == no_transition_symbol:
                            continue

                        target = self.get_state(name)

                        if target is None:
                            raise err.StateNotFoundError(name)

                        self.add_transition(
                            state, target,
                            when if when != empty_string_symbol else None)
            except Exception as e:
                self.reset()

                raise e

        return self

    def reset(self) -> None:
        """Remove all states and transitions from this automaton."""
        self.__initial_state = None

        self.__states = []
        self.__transitions = []

    @property
    def states(self) -> List[State]:
        """
        List all the states of this automaton.

        Returns
        -------
        List[Transition]
            A list containing the instances of all the states of this
            automaton.
        """
        return self.__states

    @property
    def transitions(self) -> List[Transition]:
        """
        List all the transitions of this automaton.

        Returns
        -------
        List[Transition]
            A list containing the instances of all the transitions of
            this automaton.
        """
        return self.__transitions
