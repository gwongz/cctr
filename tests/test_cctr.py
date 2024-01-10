"""End to end tests for cctr"""

import subprocess

def test_character_substitution():
    """Verify simple character substitution"""
    input_args = ['echo', 'hh']
    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    result = subprocess.check_output(["cctr", "h", "j"], stdin=ps.stdout, text=True)

    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    target = subprocess.check_output(["tr", "h", "j"], stdin=ps.stdout, text=True)

    assert result == target == "jj\n"

def test_character_substitution_when_destination_size_is_smaller_than_source():
    """Verify target set is padded"""
    input_args = ['echo', 'hi']
    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    result = subprocess.check_output(["cctr", "hm", "j"], stdin=ps.stdout, text=True)

    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    target = subprocess.check_output(["tr", "hm", "j"], stdin=ps.stdout, text=True)

    assert result == target == "ji\n"

def test_character_substitution_when_destination_size_is_greater_than_source():
    """Verify destination set is truncated"""
    input_args = ['echo', 'hiX']
    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    result = subprocess.check_output(["cctr", "h", "jkop"], stdin=ps.stdout, text=True)

    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    target = subprocess.check_output(["tr", "h", "jkop"], stdin=ps.stdout, text=True)

    assert result == target == "jiX\n"

def test_a_to_z_range_substitution_when_destination_size_is_smaller_than_source():
    """Verify a-z is expanded to ascii.lowercase and characters default to last """
    input_args = ['echo', 'aiz']
    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    result = subprocess.check_output(["cctr", "a-z", "jkop"], stdin=ps.stdout, text=True)

    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    target = subprocess.check_output(["tr", "a-z", "jkop"], stdin=ps.stdout, text=True)

    assert result == target == "jpp\n"

def test_a_to_z_range_subsitution_when_destination_size_is_larger_than_source():
    """Verify a-z is expanded and limited to size of source"""
    input_args = ['echo', 'acz']
    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    result = subprocess.check_output(["cctr", "c", "a-z"], stdin=ps.stdout, text=True)

    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    target = subprocess.check_output(["tr", "c", "a-z"], stdin=ps.stdout, text=True)

    assert result == target == "aaz\n"

def test_a_to_z_range_to_range_of_equal_size_substitution():
    """Verify a-z is expanded to ascii.lowercase and last character in destination is duplicated"""
    input_args = ['echo', 'hi']
    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    result = subprocess.check_output(["cctr", "a-z", "A-Z"], stdin=ps.stdout, text=True)

    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    target = subprocess.check_output(["tr", "a-z", "A-Z"], stdin=ps.stdout, text=True)

    assert result == target == "HI\n"

def test_lower_class_specifier():
    """Verify [:lower:] is expanded to ascii.lowercase"""
    input_args = ['echo', 'HELLO']
    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    result = subprocess.check_output(["cctr", "A-Z", "[:lower:]"], stdin=ps.stdout, text=True)

    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    target = subprocess.check_output(["tr", "A-Z", "[:lower:]"], stdin=ps.stdout, text=True)

    assert result == target == "hello\n"

def test_upper_class_specifier():
    """Verify [:upper:] is expanded to ascii.uppercase"""
    input_args = ['echo', 'hello!']
    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    result = subprocess.check_output(["cctr", "a-z", "[:upper:]"], stdin=ps.stdout, text=True)

    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    target = subprocess.check_output(["tr", "a-z", "[:upper:]"], stdin=ps.stdout, text=True)

    assert result == target == "HELLO!\n"

def test_alnum_class_specifier():
    """Verify [:alnum:] is expanded to include all alphanumeric characters"""
    input_args = ['echo', 'hello!']
    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    result = subprocess.check_output(["cctr", "[:alnum:]", "x"], stdin=ps.stdout, text=True)

    ps = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    target = subprocess.check_output(["tr", "[:alnum:]", "x"], stdin=ps.stdout, text=True)

    assert result == target == "xxxxx!\n"
