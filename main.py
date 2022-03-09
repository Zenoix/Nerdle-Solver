import re
from itertools import groupby, product
from typing import Union


class Solver:
    def __init__(self) -> None:
        self.__eq_index: int = -1
        self.__poss_patterns: list[list[str]] = [
            [".", ".", ".", ".", ".", "=", ".", "."],
            [".", ".", ".", ".", "=", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", "=", "."]
        ]
        self.__possible_chars: set = set("1234567890+-*/")
        self.__operators: set = {"+", "-", "*", "/", "="}

    def __find_eq_index(self) -> None:
        eq_index = int(input(
            "Which location did you put the equals sign? ")) - 1
        eq_correct = input("Is it in the correct position? Y/N: ")
        if eq_correct.lower() == "y":
            for pattern in self.__poss_patterns:
                if pattern[eq_index] == "=":
                    self.__poss_patterns = [pattern]
            self.__eq_index = eq_index
        else:
            self.__poss_patterns = [
                patt for patt in self.__poss_patterns
                if patt[eq_index] != "="]

    def __update_possible_chars(self):
        pass

    def __validate_lhs(self, pattern: list[str], lhs: tuple[str]) -> bool:
        cons_ops = any(
            len(list(g)) > 1 for k, g in groupby(lhs) if k in self.__operators
        )
        conditions = [
                        lhs[0] not in "0+-*/",
                        cons_ops,
                        re.match("".join(pattern), "".join(lhs))
                    ]
        return all(conditions)

    def __find_possible_solutions(self, poss_patterns: list[list[str]], poss_chars: str) -> None:
        poss_num = set(poss_chars) - self.__operators
        for pattern in poss_patterns:
            if self.__eq_index != -1:
                lhs_len = pattern.index("=")
            else:
                lhs_len, rhs_len = self.__eq_index, 7 - self.__eq_index
            for lhs in product(poss_chars, repeat=lhs_len):
                if self.__validate_lhs(self, pattern, lhs):
                    for rhs in product(poss_num, repeat=rhs_len):
                        if eval("".join(lhs)) == eval("".join(rhs)):
                            print("".join(lhs) + "=" + "".join(rhs))

    def solve(self) -> None:
        for i in range(6):
            if self.__eq_index == -1:
                self.__find_eq_index()


if __name__ == "__main__":
    solver = Solver()
    solver.solve()
