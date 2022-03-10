class WildCard:
    """Wildcard to be used as an 'any character' character."""

    __slots__ = ()

    def __eq__(self, other: str) -> bool:
        """
        As a wildcard character, it returns True
        when compared to any character.

        Arguments:
        other -- The other character
        """
        return True

    def __str__(self) -> str:
        return "'_'"

    def __repr__(self) -> str:
        return "'_'"
