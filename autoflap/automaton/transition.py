"""
Transition Between States of a Finite State Automaton
=====================================================

A transition between states of an automaton can occur between two
different states or a single state. In the latter case, the current
state of the automaton remains the same.

It is activated in a state according to the character received at its
entry. This character, however, can be a null character, also called an
empty character, which is represented by the lowercase Greek letters
epsilon `ε` or lambda `λ` in JFLAP.

From the point of view of a single state, several transitions can start
from it, and it is even possible to have a transition for each character
of the alphabet. It is not strictly mandatory for a state to participate
in at least one transition, but this would make no sense at all.
"""
__all__ = ['Transition']

from typing import Optional, Text

from .state import State


class Transition():
    """
    Store information about a specific transition between two states of
    an automaton, or between a state itself.

    A transition has three pieces of information, which are the states
    of origin and target, which can also be the same state for both, and
    the condition that must be satisfied for the transition to be
    carried out.

    For cases where the target state of the transition is the same as
    the origin state, the `target` attribute of this instance can be set
    to `None`. The same procedure applies when the condition string,
    which is stored in the `when` attribute, is empty.
    """
    def __init__(self,
                 origin: State,
                 target: Optional[State] = None,
                 when: Optional[Text] = None) -> None:
        """
        Create a new transition between two states or a state itself.

        Parameters
        ----------
        origin : State
            The instance of the origin state.
        target : Optional[State], optional
            The instance of the target state. If it is `None`, then it
            will be the origin state itself. Defaults to `None`.
        when : Optional[Text], optional
            A condition string for this transition, to define when it
            should be activated, or `None` if it is empty. Defaults to
            `None`.

        Raises
        ------
        TypeError
            Either the origin or the target is not a state instance.
        """
        if not isinstance(origin, State):
            raise TypeError('origin is not a state instance')

        self.__origin = origin

        self.target = target

        self.__when = None if not when else str(when)

    @property
    def origin(self) -> State:
        """
        Return the instance of the origin state of this transition.

        Returns
        -------
        State
            The instance of the origin state of this transition.
        """
        return self.__origin

    @property
    def target(self) -> State:
        """
        Return the instance of the target state of this transition.

        Returns
        -------
        State
            The instance of the target state of this transition.
        """
        return self.__target

    @target.setter
    def target(self, target: Optional[State]) -> None:
        """
        Set the target state of this transition.

        Parameters
        ----------
        target : Optional[State]
            The instance of the target state. If it is `None`, then it
            will be the origin state itself.

        Raises
        ------
        TypeError
            The target is not `None` and is not a state instance.
        """
        if target is None:
            target = self.origin
        elif not isinstance(target, State):
            raise TypeError('target is not a state instance')

        self.__target = target

    @property
    def when(self) -> Optional[Text]:
        """
        Return the condition string of this transition, if defined.

        Returns
        -------
        Optional[Text]
            The condition string of this transition, or `None` if it is
            empty.
        """
        return self.__when
