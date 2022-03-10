class WildCard:
    """Wildcard to be used as an 'any character' character."""
    def __eq__(self, _: str) -> bool:
        """
        As a wildcard character, it returns True
        when compared to any character.

        Arguments:
        _ -- The other character
        """
        return True

    def __str__(self) -> str:
        return "'_'"

    def __repr__(self) -> str:
        return "'_'"
