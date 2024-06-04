"""
This module contains the classes that represent Obsidian adder operators.

Operators make it possible to create very specific ways to adding content to notes.
They are generally used together with AdderWhere.
"""


from abc import ABC, abstractmethod
import re
import textwrap
from typing import Any, Self

class Op(ABC):
    """Base class for all adder operators."""
    def __init__(self: Self, operator: str):
        self.__raw_operator = operator
        self.__operator = self.build_operator(operator)
    
    @property
    def operator(self: Self) -> Any:
        return self.__operator

    @property
    @abstractmethod
    def id(self: Self) -> str:
        """The identifier of the operator."""
        ...

    @abstractmethod
    def __repr__(self: Self) -> str:
        ...
    
    @abstractmethod
    def build_operator(self: Self, operator: str) -> Any:
        """Build the operator.

        Parameters
        ----------
        operator : str
            The operator string.

        Returns
        -------
        Any
            The operator.
        """
        ...

class OpMkHeader(Op):
    def __init__(self: Self, operator: str):
        self.__raw_operator = operator
        self.__operator = self.build_operator(operator)
    
    @property
    def operator(self: Self) -> dict[str, str]:
        return self.__operator

    @property
    def id(self: Self) -> str:
        return 'mkheader'

    def __repr__(self: Self) -> str:
        return f"OperatorMkHeader('{self.__raw_operator}')"
    
    def build_operator(self: Self, operator: str) -> dict[str, str]:
        pattern = r'([\<\>]?\|[\<\>]?)\{([0-9]+)\}h([1-6])'
        match  = re.match(pattern, operator)
        if match is None:
            raise ValueError(f"Invalid operator: '{operator}'", "Must be pattern like '([\<\>]?\|[\<\>]?)\{([0-9]+)\}h([1-6])'. Example: '|>{1}h1'")
        elif len(match[1]) != 2:
            message = f"Invalid operator in '{operator}'. Must be '|>' or '<|'."
            message = message + '\n' + textwrap.dedent("In your case, it should be '|>{")
            message = message + f"{match[3]}" + "}" + f"h{match[2]}' or '<|" + "{" + f"{match[3]}" + "}" + f"h{match[2]}'"
            raise ValueError(message)
        else:
            return {
            'precedence': str(match[1]),
            'level': str(match[3]),
            'index': str(match[2])
        }
