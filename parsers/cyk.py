from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass, field
from itertools import product
from math import ceil
from typing import Dict, Hashable, List, NewType, Union, cast

import pytest

Terminal = Hashable
Variable = NewType("Variable", str)
Start: Variable = cast(Variable, object())  # Note: intentional invalid type coercing
Empty = object()
Right = Union[Terminal, tuple[Variable, Variable]]  # right side of a production rule
EMPTY_SET: set[Variable] = set()


@dataclass(frozen=True)
class Production:
    """Production rule in Chomsky Normal Form.

    Under this representation, every rule will either produce a terminal, or
    the concatenation of two variables.
    """

    left: Union[Variable]
    right: Right


@dataclass
class Grammar:
    rules: List[Production]
    reverse_map: Dict[Right, set[Variable]] = field(init=False)

    def __post_init__(self) -> None:
        all_left_variables = set(rule.left for rule in self.rules)
        assert Start in all_left_variables, "At least one rule should use Start"

        produce_variables = [rule.right for rule in self.rules if isinstance(rule.right, tuple)]
        all_right_variables = set(right[0] for right in produce_variables) & set(right[1] for right in produce_variables)
        missing = all_right_variables - all_left_variables
        assert not missing, f"{missing} missing production rules"

        reverse_map: dict[Right, set[Variable]] = {rule.right: set() for rule in self.rules}
        for rule in self.rules:
            reverse_map[rule.right].add(rule.left)

        self.reverse_map = reverse_map


def arithmetic_progression_sum(start: int, end: int, steps: int) -> int:
    assert end >= start
    assert steps >= 1
    return ceil(((start + end) * steps) / 2)


class ProductionTable:
    """Determines which variables can produce the substring"""

    def __init__(self, sentence_length: int) -> None:
        assert sentence_length >= 0

        number_of_possible_substrings = arithmetic_progression_sum(
            start=1,
            end=sentence_length,
            steps=sentence_length,
        )
        table: list[set[Variable]] = [set() for _ in range(number_of_possible_substrings)]

        self._sentence_length = sentence_length
        self._table = table

    def _pos(self, substr_start: int, substr_len: int) -> int:
        assert 0 <= substr_start
        assert 1 <= substr_len
        substr_end = substr_start + substr_len
        assert substr_end <= self._sentence_length

        if substr_len <= 2:
            offset = 0
        else:
            offset = arithmetic_progression_sum(
                start=0,
                end=substr_len - 1,
                steps=substr_len - 2,
            )

        base = self._sentence_length * (substr_len - 1)
        return base + substr_start - offset

    def entry(self, substr_start: int, substr_len: int) -> set[Variable]:
        return self._table[self._pos(substr_start, substr_len)]

    def __str__(self) -> str:
        elements = [str(entry) if entry else "{}" for entry in self._table]
        max_len_elements = max(map(len, elements))
        formatted_elements = [f"{el:>{max_len_elements}}" for el in elements]
        start = 0
        formatted_lines = []
        for qty_entries in range(self._sentence_length, 0, -1):
            end = start + qty_entries
            formatted_lines.append(" | ".join(formatted_elements[start:end]))
            start = end

        max_len_line = len(formatted_lines[0])
        formatted_table = [f"[ {line:<{max_len_line}} ]" for line in formatted_lines]
        return "\n".join(formatted_table)


def is_empty_valid(grammar: Grammar) -> bool:
    return any(rule.right is Empty and rule.left is Start for rule in grammar.rules)


def is_valid_sentence(sentence: Collection[Terminal], grammar: Grammar) -> bool:
    if len(sentence) == 0:
        return is_empty_valid(grammar)

    sentence_length = len(sentence)
    table = ProductionTable(sentence_length)

    # Populate the production table with the rules for terminal values.
    #
    # This takes advantage of the Chomsky Normal Form and only iterates over
    # the rules in the form `A -> a`, i.e. rules that produce terminals.
    for pos, token in enumerate(sentence):
        table.entry(pos, 1).update(grammar.reverse_map[token])

    # Gradually expand the table with substrings up to the whole sentence.
    #
    # Here too the algorithm relies on Chomsky Normal Form, this time it only
    # iterates over the rules in the form `A -> BC`, i.e. composed rules.
    for subsentence_length in range(2, sentence_length + 1):
        for left_start in range(0, sentence_length - subsentence_length + 1):
            for left_len in range(1, subsentence_length):
                right_start = left_start + left_len
                right_len = subsentence_length - left_len
                assert right_len >= 1
                variables = product(
                    table.entry(left_start, left_len),
                    table.entry(right_start, right_len),
                )
                for left, right in variables:
                    for variable in grammar.reverse_map.get((left, right), EMPTY_SET):
                        table.entry(left_start, subsentence_length).add(variable)

    # Check the table entry that covers the whole string
    return Start in table.entry(0, sentence_length)


def test_is_valid_sentence() -> None:
    grammar_one = Grammar(
        rules=[
            Production(Start, ("A", "B")),
            Production(Start, ("A", "C")),
            Production(Variable("A"), ("B", "A")),
            Production(Variable("A"), "a"),
            Production(Variable("B"), ("C", "C")),
            Production(Variable("B"), "b"),
            Production(Variable("C"), ("A", "B")),
            Production(Variable("C"), "c"),
        ]
    )
    assert not is_valid_sentence("", grammar_one)
    assert is_valid_sentence("ab", grammar_one)
    assert is_valid_sentence("bab", grammar_one)
    assert is_valid_sentence("ccab", grammar_one)

    grammar_two = Grammar(
        rules=[
            Production(Start, ("A", "B")),
            Production(Start, ("B", "C")),
            Production(Variable("A"), ("B", "A")),
            Production(Variable("A"), "a"),
            Production(Variable("B"), ("C", "C")),
            Production(Variable("B"), "b"),
            Production(Variable("C"), ("A", "B")),
            Production(Variable("C"), "a"),
        ]
    )
    assert not is_valid_sentence("", grammar_two)
    assert is_valid_sentence("baaba", grammar_two)


def test_production_table() -> None:
    # pylint: disable=protected-access
    assert len(ProductionTable(1)._table) == 1
    assert len(ProductionTable(2)._table) == 3
    assert len(ProductionTable(3)._table) == 6
    assert len(ProductionTable(4)._table) == 10
    assert len(ProductionTable(5)._table) == 15

    assert ProductionTable(1)._pos(0, 1) == 0
    assert ProductionTable(2)._pos(0, 1) == 0
    assert ProductionTable(2)._pos(1, 1) == 1
    assert ProductionTable(2)._pos(0, 2) == 2
    assert ProductionTable(3)._pos(0, 1) == 0
    assert ProductionTable(3)._pos(1, 1) == 1
    assert ProductionTable(3)._pos(2, 1) == 2
    assert ProductionTable(3)._pos(0, 2) == 3
    assert ProductionTable(3)._pos(1, 2) == 4
    assert ProductionTable(3)._pos(0, 3) == 5
    assert ProductionTable(4)._pos(0, 1) == 0
    assert ProductionTable(4)._pos(1, 1) == 1
    assert ProductionTable(4)._pos(2, 1) == 2
    assert ProductionTable(4)._pos(3, 1) == 3
    assert ProductionTable(4)._pos(0, 2) == 4
    assert ProductionTable(4)._pos(1, 2) == 5
    assert ProductionTable(4)._pos(2, 2) == 6
    assert ProductionTable(4)._pos(0, 3) == 7
    assert ProductionTable(4)._pos(1, 3) == 8
    assert ProductionTable(4)._pos(0, 4) == 9
    assert ProductionTable(5)._pos(0, 1) == 0
    assert ProductionTable(5)._pos(1, 1) == 1
    assert ProductionTable(5)._pos(2, 1) == 2
    assert ProductionTable(5)._pos(3, 1) == 3
    assert ProductionTable(5)._pos(4, 1) == 4
    assert ProductionTable(5)._pos(0, 2) == 5
    assert ProductionTable(5)._pos(1, 2) == 6
    assert ProductionTable(5)._pos(2, 2) == 7
    assert ProductionTable(5)._pos(3, 2) == 8
    assert ProductionTable(5)._pos(0, 3) == 9
    assert ProductionTable(5)._pos(1, 3) == 10
    assert ProductionTable(5)._pos(2, 3) == 11
    assert ProductionTable(5)._pos(0, 4) == 12

    with pytest.raises(AssertionError):
        ProductionTable(1)._pos(1, 0)

    with pytest.raises(AssertionError):
        ProductionTable(1)._pos(1, 1)

    with pytest.raises(AssertionError):
        ProductionTable(1)._pos(0, 2)

    with pytest.raises(AssertionError):
        ProductionTable(2)._pos(1, 2)
