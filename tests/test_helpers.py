
from pyobsidian.helpers import *

def test_convert_str_or_list_to_list_string():
    assert convert_str_or_list_to_list('string') == ['string']

def test_convert_str_or_list_to_list_list():
    assert convert_str_or_list_to_list(['list']) == ['list']

def test_has_yaml_true_when_has_yaml():
    markdown = """
    ---
    property: value
    ---
    """
    assert has_yaml(markdown)

def test_has_yaml_false_when_has_no_yaml():
    markdown = """
    property: value
    """
    assert not has_yaml(markdown)
