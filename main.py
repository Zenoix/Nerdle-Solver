import re
import itertools
from typing import Union


class Solver:
    def __init__(self) -> None:
        self.__eq_index_found: bool = False
        self.__poss_patterns: list[list[Union[None, str]]] = [
            [None, None, None, None, None, "=", None, None],
            [None, None, None, None, "=", None, None, None],
            [None, None, None, None, None, None, "=", None]
        ]
        self.__possible_chars: set = set("1234567890+-*/")

    # def __find_possible_solutions(self, poss_patterns: list, poss_chars: str) -> None:
    #     poss_num = set(poss_chars) - {"+", "-", "*", "/", "="}
    #     rhs_len = 7 - lhs_len
    #     for lhs in itertools.product(poss_chars, repeat=lhs_len):
    #         if lhs[0] in "0+-*/":
    #             pass
    #         for rhs in itertools.product(poss_num, repeat=rhs_len):
    #             if eval("".join(lhs)) == eval("".join(rhs)):
    #                 print("".join(lhs) + "=" + "".join(rhs))

    def __find_eq_index(self):
        eq_index = int(input(
            "Which location did you put the equals sign? ")) - 1
        eq_correct = input("Is it in the correct position? Y/N: ")
        if eq_correct.lower() == "y":
            for pattern in self.__poss_patterns:
                if pattern[eq_index] == "=":
                    self.__poss_patterns = [pattern]
            self.__eq_index_found = True
            print(self.__poss_patterns)
        else:
            self.__poss_patterns = [
                patt for patt in self.__poss_patterns
                if patt[eq_index] != "="]
            print(self.__poss_patterns)

    def solve(self):
        for i in range(6):
            if not self.__eq_index_found:
                self.__find_eq_index()


if __name__ == "__main__":
    solver = Solver()
    solver.solve()
