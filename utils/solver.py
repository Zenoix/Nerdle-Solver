from collections import defaultdict, Counter
from itertools import product
from re import search
import sys
import time

from utils.wildcard import WildCard


class Solver:
    """
    The Nerdle solver class.

    Methods
    -------
    solve()
        Prints the most optimal first and second guesses.
        Starting with the second guess, it starts printing all
        possible guesses.
    """

    def __init__(self) -> None:
        w = WildCard()  # WildCard matches with any character except for "="

        # Initiate the starting possible patterns (in relation to the "=")
        self.__poss_patterns: list[list[str]] = [
            [w, w, w, w, w, "=", w, w],
            [w, w, w, w, "=", w, w, w],
            [w, w, w, w, w, w, "=", w]
        ]

        self.__eq_index: int = -1  # The index of "=" if found otherwise -1
        # Key: Possible numbers, Value: max number of occurances
        self.__nums: dict[str, int] = {k: 7 for k in "1234567890"}
        # Key: Possible operators, Value: max number of occurances
        self.__operators: dict[str, int] = {k: 7 for k in "+-*/"}
        self.__guesses: list[str] = []  # Used guesses, prevents repeats
        # Characters that must be contained in the guess
        self.__must_contain: set[str] = set()
        # Characters that cannot occur at the corresponding index
        self.__invalid_location: list[list[str]] = [[] for _ in range(8)]

    def __find_eq_index(self, eq_index: int) -> None:
        """
        Sets matched pattern and equal sign index if equal sign is found.
        Otherwise, it eliminates impossible patterns if equal sign does
        does not match the pattern.

        Parameters
        ----------
        eq_index : int
            The index of the equal sign in the guess
        """

        eq_correct = input("Is the equals sign in the correct position? Y/N: ")
        if eq_correct.lower() in ("y", "yes"):
            # If the equals sign has been found, all other patterns do not work
            for pattern in self.__poss_patterns:
                if pattern[eq_index] == "=":
                    # Set "self.__poss_patterns" to correct pattern
                    self.__poss_patterns = [pattern]
                    break
            self.__eq_index = eq_index
        else:
            # Remove the patterns that have the equals sign in the wrong place
            self.__poss_patterns = [
                patt for patt in self.__poss_patterns
                if patt[eq_index] != "="]

    def __update_possible_chars(self) -> None:
        """
        Updates the patterns and/or dictionaries containing
        the possible characters.
        """

        prompt = "What color was '{}' at position '{}'? (G)reen/(P)urple/(B)lack: "
        # Keep track of maximum possible occurances of each character used more than one
        counts = defaultdict(int)

        used_equation = input("What equation did you use? ").strip()
        while len(used_equation) != 8:
            used_equation = input(
                "Invalid equation, try again. What equation did you use? ").strip()

        if input(f"Was {used_equation} the correct answer? Y/N: ").strip().lower() in ("y", "yes"):
            print("Congratulations!")
            sys.exit()

        self.__guesses.append(used_equation)
        for idx, char in enumerate(used_equation):
            if char == "=":
                # If the index of equal sign
                if self.__eq_index == -1:
                    self.__find_eq_index(idx)
                continue
            match input(prompt.format(char, idx + 1)).strip().lower():
                case "green | g":
                    # If we found a green, add char to all patterns at that index
                    for pattern in self.__poss_patterns:
                        pattern[idx] = char
                    counts[char] += 1
                    # If char is green, it must be contained in generated guess
                    self.__must_contain.add(char)
                case "purple | p":
                    counts[char] += 1
                    self.__invalid_location[idx].append(
                        char)  # Char cannot be at that index
                    # If char is purple, it must be contained in generated guess
                    self.__must_contain.add(char)
                case "black" | "b" if char in self.__nums:
                    # If number is black, but occured before, than the count
                    # is the max occurance of that number
                    if char in counts:
                        self.__nums[char] = counts[char]
                    else:
                        # If the number does not exist,
                        # remove from possible numbers
                        del self.__nums[char]
                case "black" | "b" if char in self.__operators:
                    if char in counts:
                        # If operator is black, but occured before, than the count
                        # is the max occurance of that operator
                        self.__operators[char] = counts[char]
                    else:
                        # If the operator does not exist,
                        # remove from possible operators
                        del self.__operators[char]

    def __find_possible_guesses(self) -> list[str]:
        """
        Generates all possible guesses that satify the patterns
        with the valid characters in the dictionaries.

        Returns
        -------
        possible : list[str]
            A list containing all possible guesses
        """
        possible = []
        time_start = time.perf_counter()  # Start time
        for pattern in self.__poss_patterns:
            # Finds the length of the left hand side
            lhs_len = pattern.index(
                "=") if self.__eq_index == -1 else self.__eq_index
            rhs_len = 7 - lhs_len  # Length of the right hand side

            # Generate all possible combinations of the left hand side
            for lhs in product((self.__nums | self.__operators).keys(), repeat=lhs_len):
                if self.__validate_lhs(pattern, lhs):
                    # Generate all possible combinations of the right hand side
                    for rhs in product(self.__nums.keys(), repeat=rhs_len):
                        lhs_str, rhs_str = "".join(lhs), "".join(rhs)
                        # Validates the whole equation
                        if self.__validate_equation(pattern, lhs_str, rhs_str):
                            possible.append(f"{lhs_str}={rhs_str}")

        time_stop = time.perf_counter()  # End time

        if len(possible) == 1:
            print(f"Only one possible solution {possible[0]}")
        else:
            print("\n".join(possible))
            print(
                f"Generated {len(possible)} combinations in {time_stop - time_start:.2f} seconds")
        return possible

    def __validate_lhs(self, pattern: list[str], lhs: tuple[str]) -> bool:
        """
        Checks that a generated left hand side of the equation is valid.

        Parameters
        ----------
        pattern : list[str]
            Pattern to check the left hand side against
        lhs : tuple[str]
            A generated left hand side of the equation to check

        Returns
        -------
        _ : bool
            True if the generated left hand side is valid
            False if the generated left hand side is invalid
        """

        # Regex pattern checks division by zero, leading zeros,
        # lone zeros, and consecutive operators
        regex_pattern = r"/0$|/0[+\-/*]|[+\-*/]0\d|[+\-*/]0[+\-*/]|[+\-*/]{2,}"
        valid_conditions = [
            lhs[0] not in "0+-*/",
            lhs[-1] not in "+-*/",
            lhs[-2:] != ("/", "0"),
            not search(regex_pattern, "".join(lhs)),
            pattern[:pattern.index("=")] == list(lhs)
        ]
        return all(valid_conditions)

    def __validate_equation(self, pattern: list[str], lhs_str: str, rhs_str: str) -> bool:
        """
        Checks that the whole generated equation is valid.

        Parameters
        ----------
        pattern : list[str]
            Pattern to check the equation against
        lhs_str : str
            String version of the generated left hand side to check
        rhs_str : str
            String version of the generated right hand side to check

        Returns
        -------
        _ : bool
            True if the generated equation is valid
            False if the generated equation is invalid
        """

        equation = f"{lhs_str}={rhs_str}"

        # Counts the total max number of character occurances
        possible_char_counter = Counter(self.__nums | self.__operators)
        # Counts character occurances in the generated equation
        equation_counter = Counter(lhs_str + rhs_str)
        # (max - observed) counts
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
        """
        Updates the patterns if there are positions
        where there's only one possible character.

        Parameters
        ----------
        generated_guesses : list[str]
            List of all generated possible guesses from the current round
        """

        for i in range(8):
            first = generated_guesses[0][i]
            if all(guess[i] == first for guess in generated_guesses):
                for pattern in self.__poss_patterns:
                    pattern[i] = first

    def solve(self) -> None:
        """Runner code for solving Nerdle."""

        for i in range(6):
            # Optimal first guess
            if i == 0:
                print("Guess 1: 9*8-7=65")
            # Optimal second guess
            elif i == 1:
                print("Guess 2: 0+12/3=4")
            self.__update_possible_chars()
            print("-" * 30)
            # Generate guesses on the second round
            if i != 0:
                print("Generated possible guesses:")
                possible_guesses = self.__find_possible_guesses()
                self.__update_patterns_from_possible_guesses(possible_guesses)
                print("-" * 30)
            print()
