"""Python script for implement tr command"""
import re
import string
import sys
from enum import Enum


import constants

class Mode(Enum):
    """Enum to determine whether to substitute, squeeze or delete characters"""
    DELETE = "1"
    SQUEEZE = "2"
    SUBSTITUTE = "3"

CHARACTER_SPECIFIER_MAP = {
    "upper": string.ascii_uppercase,
    "lower": string.ascii_lowercase,
    "alnum": f"{string.digits}{string.ascii_uppercase}{string.ascii_lowercase}",
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

    Only supports ascii character ranges
    """
    def __init__(self, raw_value):
        self.value = raw_value

    def expand(self):
        """Expands characters in a range"""
        list_of_chars = [chr(x) for x in range(ord(self.value[0]), ord(self.value[2]) + 1)]
        chars = ''.join(list_of_chars)
        return chars


class ClassExpander(Expander):
    """
    Concrete class for substitutions represented by a character class.
    For example, "[:upper:]"
    """

    def __init__(self, raw_value):
        self.value = raw_value

    def _get_class_name(self):
        pattern = r'[a-z]+'
        match = re.search(pattern, self.value)
        return match.group()

    def _is_valid_class(self, class_name):
        return class_name in CHARACTER_SPECIFIER_MAP

    def expand(self):
        class_name = self._get_class_name()
        if not self._is_valid_class(class_name):
            raise ValueError("Invald class specifier")
        return CHARACTER_SPECIFIER_MAP.get(class_name)


class SimpleExpander(Expander):
    """Basic character substitution"""
    def __init__(self, raw_value):
        self.value = raw_value

    def expand(self):
        return self.value


def substitute():
    """Copies the standard input to the standard output with substitution of selected characters """
    if is_class_specifier(constants.SOURCE):
        source_expander = ClassExpander(constants.SOURCE)
    elif is_range_specifier(constants.SOURCE):
        source_expander = RangeExpander(constants.SOURCE)
    else:
        source_expander = SimpleExpander(constants.SOURCE)

    if is_class_specifier(constants.DESTINATION):
        destination_expander = ClassExpander(constants.DESTINATION)
    elif is_range_specifier(constants.DESTINATION):
        destination_expander = RangeExpander(constants.DESTINATION)
    else:
        destination_expander = SimpleExpander(constants.DESTINATION)

    pattern = source_expander.expand()
    target = destination_expander.expand()

    if len(pattern) > len(target):
        pad_count = len(pattern) - len(target)
        target = f"{target}{target[-1] * pad_count}"
    elif len(pattern) < len(target):
        limit = len(pattern)
        target = target[:limit]

    tr_map = str.maketrans(pattern, target)

    while True:
        line = sys.stdin.readline()
        if not line:
            break
        output = line.translate(tr_map)
        print(output, end="")

def delete():
    """Delete all characters in source set"""
    print(f"These are the characters to delete: {constants.SOURCE}")

    chars_to_delete = {char: None for char in constants.SOURCE}
    tr_map = str.maketrans(chars_to_delete)
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        output = line.translate(tr_map)
        print(output, end="")

if __name__ == '__main__':
    if constants.MODE == Mode.SUBSTITUTE.value:
        substitute()
    elif constants.MODE == Mode.DELETE.value:
        delete()
    elif constants.MODE == Mode.SQUEEZE.value:
        raise NotImplementedError("Squeeze is not implemented yet")
