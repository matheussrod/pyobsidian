
from pyobsidian.filter import Field

def test_propertie_key(field):
    assert field.key == 'content'

def test_propertie_value(field):
    assert field.value == 'value'

def test_propertie_mode(field):
    assert field.occurrence == 'file'

def test__eq__(field):
    new_field = Field('content', 'value', 'file')
    assert field == new_field

def test__eq__not_field(field):
    new_field = 'field'
    assert not field == new_field