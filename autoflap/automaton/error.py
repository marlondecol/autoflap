"""
Custom Exception Classes
========================

These are all the custom exception classes raised during the execution
of this application or in the automata, states and transitions
handling.

Every class extends the `AutomatonError` class, with the exception of
itself, which extends the built-in `Exception` class. In addition, every
class assigns, by default, a generic error message, expressing the
exception that occurred, which can be manually overwritten when raising
it.
"""
__all__ = [
    'AutomatonError', 'HeadersNotFoundError',
    'InitialStateAlreadyDefinedError', 'InvalidStateNameError',
    'NoFinalStateError', 'NoInitialStateError', 'StateExistsError',
    'StateNotFoundError', 'TransitionExistsError'
]

from typing import List, Optional, Text


class AutomatonError(Exception):
    """
    Fundamental exception of automaton. It can be raised when a generic
    error occurs while performing an operation related to an automaton.

    This class extends the built-in `Exception` class, which allows you
    to set an error message when raised.
    """
    def __init__(self, message: Text = '') -> None:
        """
        Fundamental exception of automaton.

        Parameters
        ----------
        message : Text, optional
            An error message for the exception. Defaults to `''`.
        """
        super().__init__(message or 'unknown error')


class HeadersNotFoundError(AutomatonError):
    """
    Exception class for when the headers of the input CSV file are not
    found.

    This class extends the `AutomatonError` class.
    """
    def __init__(self) -> None:
        """Headers not found in the input CSV file."""
        super().__init__('no headers were found')


class InitialStateAlreadyDefinedError(AutomatonError):
    """
    Exception class for when the initial state of an automaton is
    already defined when parsing an input CSV file.

    This class extends the `AutomatonError` class.
    """
    def __init__(self, initial_state_name: Text) -> None:
        """
        An initial state is already defined.

        Parameters
        ----------
        initial_state_name : Text
            The name of the current initial state.
        """
        self.initial_state_name = initial_state_name

        super().__init__(f'initial state already defined: ' \
                         f'{self.initial_state_name}')


class InvalidStateNameError(AutomatonError):
    """
    Exception class for when an attempt is made to name a state with a
    null or empty name, which is invalid.

    This class extends the `AutomatonError` class.
    """
    def __init__(self) -> None:
        """The state name is invalid."""
        super().__init__('the state name cannot be null or empty')


class NoFinalStateError(AutomatonError):
    """
    Exception class for when the automaton has no final state when
    exporting it to a JFLAP design file.

    This class extends the `AutomatonError` class.
    """
    def __init__(self) -> None:
        """There is no final state."""
        super().__init__('the automaton does not have a final state')


class NoInitialStateError(AutomatonError):
    """
    Exception class for when the automaton does not have an initial
    state when exporting it to a JFLAP design file.

    This class extends the `AutomatonError` class.
    """
    def __init__(self) -> None:
        """There is no initial state."""
        super().__init__('the automaton does not have an initial state')


class StateExistsError(AutomatonError):
    """
    Exception class for when there is an attempt to add a state in which
    the name has already been used in another state of the same
    automaton.

    This class extends the `AutomatonError` class.
    """
    def __init__(self, state_name: Text) -> None:
        """
        There is already a state with this name.

        Parameters
        ----------
        state_name : Text
            The state name of the attempt.
        """
        self.state_name = state_name

        super().__init__(f'the state {self.state_name} already exists')


class StateNotFoundError(AutomatonError):
    """
    Exception class for when an attempt is made to reference a state
    that has not been added to an automaton.

    This class extends the `AutomatonError` class.
    """
    def __init__(self, state_name: Text) -> None:
        """
        State not found in the automaton.

        Parameters
        ----------
        state_name : Text
            The state name of the attempt.
        """
        self.state_name = state_name

        super().__init__(f'the state {self.state_name} was not found')


class TransitionExistsError(AutomatonError):
    """
    Exception class for when there is an attempt to add a transition in
    which both the origin state and its condition have already been used
    in another transition of the same automaton.

    This class extends the `AutomatonError` class.
    """
    def __init__(self, origin_state_name: Text, when: Optional[Text]) -> None:
        """
        A transition with this origin and this condition already exists.

        Parameters
        ----------
        origin_state_name : Text
            The origin state name of the attempt.
        when : Optional[Text]
            The condition string of the transition, or `None` if it is
            empty.
        """
        self.origin_state_name = origin_state_name
        self.when = when

        super().__init__(f'the transition from {self.origin_state_name} ' \
                         f'when {self.when} already exists')
