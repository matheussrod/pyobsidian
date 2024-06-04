
from pyobsidian.adder_op import OpMkHeader
import pytest

def test_op_mk_header():
    op_str = '|>{1}h1'
    op = OpMkHeader(op_str)

    assert op.operator == {
        'precedence': '|>', 
        'level': '1', 
        'index': '1'
    }

def test_op_mk_header_raise_error_when_invalid_operator():
    op_str = '>{1}h1'
    with pytest.raises(ValueError):
        OpMkHeader(op_str)

def test_op_mk_header_raise_error_when_invalid_precedence():
    op_str = '|{0}h1'
    with pytest.raises(ValueError):
        OpMkHeader(op_str)
