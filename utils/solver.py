from collections import defaultdict, Counter
from itertools import groupby, product
from re import match

from utils.wildcard import WildCard


class Solver:
    def __init__(self) -> None:
        self.__eq_index: int = -1
        self.__poss_patterns: list[list[str]] = [
            [".", ".", ".", ".", ".", "=", ".", "."],
            [".", ".", ".", ".", "=", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", "=", "."]
        ]
        self.__nums: dict[str, int] = {k: 7 for k in "1234567890"}
        self.__operators: dict[str, int] = {k: 7 for k in "+-*/"}
        self.__guesses: list[str] = []

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

    def __update_possible_chars(self) -> None:
        prompt = "What color was {} at position {}? Green/Purple/Gray: "
        counts = defaultdict()
        used_equation = ""
        while len(used_equation) != 8:
            used_equation = input("What equation did you use? ").strip()
            if used_equation != "":
                print("Invalid equation.")
        self.__guesses.append(used_equation)
        for i, char in enumerate(used_equation):
            if char == "=":
                continue
            color = input(prompt.format(char, i + 1)).strip().lower()
            match color:
                case "green":
                    for pattern in self.__poss_patterns:
                        pattern[i] = char
                    counts[char] += 1
                case "purple":
                    counts[char] += 1
                case "gray" if char in self.__nums:
                    if char in counts:
                        self.__nums[char] = counts[char]
                    else:
                        del self.__nums[char]
                case "gray" if char in self.__operators:
                    if char in counts:
                        self.__operators[char] = counts[char]
                    else:
                        del self.__operators[char]

    def __validate_lhs(self, pattern: list[str], lhs: tuple[str]) -> bool:
        consecutive_operators_valid = all(
            len(list(g)) == 1 for k, g in groupby(lhs) if k in self.__operators
        )
        conditions = [
            lhs[0] not in "0+-*/",
            consecutive_operators_valid,
            match("".join(pattern[:pattern.index("=")]), "".join(lhs))
        ]
        return all(conditions)

    def __validate_equation(self, lhs_str: str, rhs_str: str) -> bool:
        possible_char_counter = Counter(self.__nums | self.__operators)
        equation_counter = Counter(lhs_str + rhs_str)
        counter_diff = possible_char_counter.subtract(equation_counter)
        if len(-counter_diff):
            return False
        if len(rhs_str) > 1 and len(rhs_str) == "0":
            return False
        return eval(f"{lhs_str} == {rhs_str}") and f"{lhs_str}={rhs_str}" not in self.__guesses

    def __find_possible_solutions(self) -> None:
        for pattern in self.__poss_patterns:
            if self.__eq_index != -1:
                lhs_len = pattern.index("=")
            else:
                lhs_len, rhs_len = self.__eq_index, 7 - self.__eq_index
            for lhs in product((self.__nums | self.__operators).keys(), repeat=lhs_len):
                if self.__validate_lhs(self, pattern, lhs):
                    for rhs in product(self.__nums.keys(), repeat=rhs_len):
                        lhs_str, rhs_str = "".join(lhs), "".join(rhs)
                        if self.__validate_equation(lhs_str, rhs_str):
                            print(f"{lhs_str}={rhs_str}")

    def solve(self) -> None:
        # TODO put it all together and test it
        for i in range(6):
            if self.__eq_index == -1:
                self.__find_eq_index()
            self.__update_possible_chars()
