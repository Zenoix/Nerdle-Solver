from collections import defaultdict, Counter
from itertools import product
from re import search

from utils.wildcard import WildCard


class Solver:
    def __init__(self) -> None:
        self.__eq_index: int = -1

        w = WildCard()
        self.__poss_patterns: list[list[str]] = [
            [w, w, w, w, w, "=", w, w],
            [w, w, w, w, "=", w, w, w],
            [w, w, w, w, w, w, "=", w]
        ]

        self.__nums: dict[str, int] = {k: 7 for k in "1234567890"}
        self.__operators: dict[str, int] = {k: 7 for k in "+-*/"}
        self.__guesses: list[str] = []
        self.__must_contain: set[str] = set()
        self.__invalid_location: list[list[str]] = [[] for _ in range(8)]

    def __find_eq_index(self, eq_index: int) -> None:
        # eq_index = int(input(
        #     "Which location did you put the equals sign? ")) - 1
        eq_correct = input("Is the equals sign in the correct position? Y/N: ")
        if eq_correct.lower() in ("y", "yes"):
            for pattern in self.__poss_patterns:
                if pattern[eq_index] == "=":
                    self.__poss_patterns = [pattern]
                    break
            self.__eq_index = eq_index
        else:
            self.__poss_patterns = [
                patt for patt in self.__poss_patterns
                if patt[eq_index] != "="]

    def __update_possible_chars(self) -> None:
        prompt = "What color was '{}' at position '{}'? Green/Purple/Gray: "
        counts = defaultdict(int)
        used_equation = ""
        while len(used_equation) != 8:
            used_equation = input("What equation did you use? ").strip()
        self.__guesses.append(used_equation)
        for idx, char in enumerate(used_equation):
            if isinstance(self.__poss_patterns[0][idx], str):
                continue
            elif char == "=":
                if self.__eq_index == -1:
                    self.__find_eq_index(idx)
                continue
            color = input(prompt.format(char, idx + 1)).strip().lower()
            match color:
                case "green":
                    for pattern in self.__poss_patterns:
                        pattern[idx] = char
                    counts[char] += 1
                    self.__must_contain.add(char)
                case "purple":
                    counts[char] += 1
                    self.__invalid_location[idx].append(char)
                    self.__must_contain.add(char)
                case "gray" | "grey" if char in self.__nums:
                    if char in counts:
                        self.__nums[char] = counts[char]
                    else:
                        del self.__nums[char]
                case "gray" | "grey" if char in self.__operators:
                    if char in counts:
                        self.__operators[char] = counts[char]
                    else:
                        del self.__operators[char]

    def __find_possible_guesses(self) -> list[str]:
        possible = []
        for pattern in self.__poss_patterns:
            lhs_len = pattern.index(
                "=") if self.__eq_index == -1 else self.__eq_index
            rhs_len = 7 - self.__eq_index
            for lhs in product((self.__nums | self.__operators).keys(), repeat=lhs_len):
                if self.__validate_lhs(pattern, lhs):
                    for rhs in product(self.__nums.keys(), repeat=rhs_len):
                        lhs_str, rhs_str = "".join(lhs), "".join(rhs)
                        if self.__validate_equation(pattern, lhs_str, rhs_str):
                            possible.append(f"{lhs_str}={rhs_str}")
        if len(possible) == 1:
            print(f"Only one possible solution {possible[0]}")
        else:
            print("\n".join(possible))
        return possible

    def __validate_lhs(self, pattern: list[str], lhs: tuple[str]) -> bool:
        valid_conditions = [
            lhs[0] not in "0+-*/",
            lhs[-1] not in "+-*/",
            lhs[-2:] != ("/", "0"),
            not search(r"/0$|/0[+\-/*]|[+\-*/]0\d|[+\-*/]{2,}", "".join(lhs)),
            pattern[:pattern.index("=")] == list(lhs)
        ]
        return all(valid_conditions)

    def __validate_equation(self, pattern: list[str], lhs_str: str, rhs_str: str) -> bool:
        equation = f"{lhs_str}={rhs_str}"
        possible_char_counter = Counter(self.__nums | self.__operators)
        equation_counter = Counter(lhs_str + rhs_str)
        possible_char_counter.subtract(equation_counter)

        invalid_conditions = [
            len(-possible_char_counter),
            len(rhs_str) > 1 and len(rhs_str) == "0",
            rhs_str[0] == "0",
            pattern != list(equation),
            equation in self.__guesses
        ]
        if any(invalid_conditions):
            return False
        for idx, char in enumerate(equation):
            if char in self.__invalid_location[idx]:
                return False
        return eval(f"{lhs_str} == {rhs_str}") and all(char in equation for char in self.__must_contain)

    def __update_patterns_from_possible_guesses(self, generated_guesses: list[str]) -> None:
        for i in range(8):
            first = generated_guesses[0][0]
            if all(guess[0] == first for guess in generated_guesses):
                for pattern in self.__poss_patterns:
                    pattern[i] = first

    def solve(self) -> None:
        # TODO put it all together and test it
        for i in range(6):
            if i == 0:
                print("Suggestion: 9*8-7=65")
            elif i == 1:
                print("Suggestion: 0+12/3=4")
            self.__update_possible_chars()
            print("-" * 30)
            print("Generated possible guesses:")
            possible_guesses = self.__find_possible_guesses()
            print("-" * 30)
