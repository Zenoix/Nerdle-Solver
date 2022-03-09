from re import match
from itertools import groupby, product
from collections import defaultdict


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

    def __update_possible_chars(self):
        prompt = "What color was {} at position {}? Green/Purple/Gray: "
        counter = defaultdict()
        used_equation = ""
        while len(used_equation) != 8:
            used_equation = input("What equation did you use? ").strip()
            if used_equation != "":
                print("Invalid equation.")
        for i, char in enumerate(used_equation):
            if char == "=":
                continue
            color = input(prompt.format(char, i + 1)).strip().lower()
            match color:
                case "green":
                    for pattern in self.__poss_patterns:
                        pattern[i] = char
                    counter[char] += 1
                case "purple":
                    counter[char] += 1
                case "gray" if char in self.__nums:
                    if char in counter:
                        self.__nums[char] = counter[char]
                    else:
                        del self.__nums[char]
                case "gray" if char in self.__operators:
                    if char in counter:
                        self.__operators[char] = counter[char]
                    else:
                        del self.__operators[char]

    def __validate_lhs(self, pattern: list[str], lhs: tuple[str]) -> bool:
        # TODO use the value in the char dicts (max possible occurances) to add a validation
        cons_ops = any(
            len(list(g)) > 1 for k, g in groupby(lhs) if k in self.__operators
        )
        conditions = [
            lhs[0] not in "0+-*/",
            cons_ops,
            match("".join(pattern), "".join(lhs))
        ]
        return all(conditions)

    def __find_possible_solutions(self) -> None:
        for pattern in self.__poss_patterns:
            if self.__eq_index != -1:
                lhs_len = pattern.index("=")
            else:
                lhs_len, rhs_len = self.__eq_index, 7 - self.__eq_index
            for lhs in product(self.__nums | self.__operators, repeat=lhs_len):
                if self.__validate_lhs(self, pattern, lhs):
                    for rhs in product(self.__nums, repeat=rhs_len):
                        lhs_str, rhs_str = "".join(lhs), "".join(rhs)
                        equation = f"{lhs_str}={rhs_str}"
                        if eval(f"{lhs_str} == {rhs_str}") and equation not in self.__guesses:
                            print(equation)

    def solve(self) -> None:
        for i in range(6):
            if self.__eq_index == -1:
                self.__find_eq_index()
            self.__update_possible_chars()


if __name__ == "__main__":
    solver = Solver()
    solver.solve()
