"""Python script for implement tr command"""
import re
import string
import sys

import constants

CHARACTER_SPECIFIER_MAP = {
    "upper": string.ascii_uppercase,
    "lower": string.ascii_lowercase,
}

def is_range_specifier(specifier):
    """Determines whether a range of characters has been specified"""
    # a-z, A-z
    if len(specifier) != 3:
        return False
    if specifier[1] != '-':
        return False
    return True

def is_class_specifier(specifier):
    """Determines whether a class specifier has been specified"""
    pattern = r'^\[:[a-z]+:\]$'
    match = re.match(pattern, specifier)
    return match is not None



class Expander:
    """Interface for handling a translation"""
    def expand(self):
        """Method for creating source and destination set"""
        raise NotImplementedError


class RangeExpander(Expander):
    """
    Concrete class for subsitutions to be made for a range of characters.
    For example, "a-z"
    """
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def expand(self):
        pattern = self._expand_chars(self.source)
        target = self._expand_chars(self.destination)
        return pattern, target

    def _expand_chars(self, specifier):
        """Expands characters in a range"""
        list_of_chars = [chr(x) for x in range(ord(specifier[0]), ord(specifier[2]))]
        chars = ''.join(list_of_chars)
        return chars

class ClassExpander(Expander):
    """
    Concrete class for substitutions represented by a character class.
    For example, "[:upper:]"
    """

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def _get_class_name(self, specifier):
        pattern = r'[a-z]+'
        match = re.search(pattern, specifier)
        return match.group()

    def _is_valid_class(self, class_name):
        return class_name in CHARACTER_SPECIFIER_MAP

    def _expand_specifier(self, specifier):
        # expand lower to abcdefghijklmnopqrstuvwxyz
        return CHARACTER_SPECIFIER_MAP.get(specifier)

    def expand(self):
        source_class = self._get_class_name(self.source)
        destination_class = self._get_class_name(self.destination)
        if not self._is_valid_class(source_class):
            raise ValueError("Unsupported source specifier")
        if not self._is_valid_class(destination_class):
            raise ValueError("Unsupported destination specifier")

        pattern = self._expand_specifier(source_class)
        target = self._expand_specifier(destination_class)

        return pattern, target

class SimpleExpander(Expander):
    """Basic character substitution"""
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def expand(self):
        if len(self.source) > len(self.destination):
            padded_destination = self.destination * len(self.source)
            return self.source, padded_destination
        elif len(self.destination) > len(self.source):
            limit = len(self.source)
            return self.source, self.destination[:limit]
        return self.source, self.destination

def substitute():
    """Copies the standard input to the standard output with substitution of selected characters """
    if is_class_specifier(constants.SOURCE):
        expander = ClassExpander(constants.SOURCE, constants.DESTINATION)
    elif is_range_specifier(constants.SOURCE):
        expander = RangeExpander(constants.SOURCE, constants.DESTINATION)
    else:
        expander = SimpleExpander(constants.SOURCE, constants.DESTINATION)
    pattern, target = expander.expand()
    tr_map = str.maketrans(pattern, target)

    for line in sys.stdin:
        output = line.translate(tr_map)
        print(output)

if __name__ == '__main__':
    substitute()
