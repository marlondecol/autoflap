"""
State of a Finite State Automaton
=================================

Each point between its chain of transitions is considered to be a state
of an automaton.

A state can be, but not necessarily, initial, final or both for this
chain, and its identification must be unique among the others. A single
automaton can have as many final states as necessary, as long as it has
at least one. However, it must have exactly one initial state.

Because it is part of a chain of transitions, this state will transition
to another state depending on what is received at its entry from the
last transition, until the entire expression is computed.
"""
__all__ = ['State']

from typing import Text

from . import error as err


class State:
    """
    Allow the handling of an automaton state.

    An instance of this class can be used both to compose an automaton
    and to indicate the state of origin, target or both of a transition.

    It has only two attributes, the main one of which is its name, which
    cannot be null or empty. The other one indicates whether this is a
    final state or not for an automaton, taken as `False` by default.

    The attribute that indicates whether this state is initial or not
    for an automaton is defined directly in the instance of the latter.
    """
    def __init__(self, name: Text, is_final: bool = False) -> None:
        """
        Create a new state with a given name.

        Parameters
        ----------
        name : Text
            The name of the state.
        is_final : bool, optional
            `True` if the state is final, `False` otherwise. Defaults to
            `False`.

        Raises
        ------
        InvalidStateNameError
            The state name is null or empty.
        """
        name = str(name or '')

        if not name:
            raise err.InvalidStateNameError()

        self.__name = name

        self.is_final = is_final

    @property
    def is_final(self) -> bool:
        """
        Return whether this state is final or not.

        Returns
        -------
        bool
            `True` if this state is final, `False` otherwise.
        """
        return self.__is_final

    @is_final.setter
    def is_final(self, is_final: bool) -> None:
        """
        Set whether this state is final or not.

        Parameters
        ----------
        is_final : bool
            `True` if this state is final, `False` otherwise.
        """
        self.__is_final = bool(is_final)

    @property
    def name(self) -> Text:
        """
        Return the name string for this state.

        Returns
        -------
        Text
            The name string for this state.
        """
        return self.__name
