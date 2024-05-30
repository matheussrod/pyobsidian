
import pytest
from pyobsidian.filter import Filter

def test__len__empty_list():
    filter = Filter()
    filter_len = len(filter)
    expected_len = 0
    assert filter_len == expected_len

def test__len__list_with_n_elements(filter_field):
    filter = Filter([filter_field, filter_field, filter_field])
    filter_len = len(filter)
    expected_len = 3
    assert filter_len == expected_len

def test__eq__empty_filter():
    filter = Filter()
    new_filter = Filter()
    assert filter == new_filter

def test__eq__non_empty_filter(filter_field):
    filter = Filter([filter_field])
    new_filter = Filter().add_field(filter_field)
    assert filter == new_filter

def test__eq__different_filters(filter_field):
    filter = Filter([filter_field])
    new_filter = Filter()
    assert filter != new_filter

def test__eq__not_filter_instance():
    filter = Filter()
    x = 'filter'
    assert not filter == x

def test__next__empty_list():
    with pytest.raises(StopIteration):
        filter = Filter()
        filter_iter = iter(filter)
        next(filter_iter)

def test__next__non_empty_list(filter_field):
    filter = Filter([filter_field])
    next_filter_field = next(iter(filter))
    assert next_filter_field == filter_field

def test_propertie_fields(filter_field):
    filter = Filter([filter_field])
    filter_fields = filter.fields
    expected_fields = [filter_field]
    assert filter_fields == expected_fields

def test_add_field(filter_field):
    filter = Filter()
    new_filter = filter.add_field(filter_field)
    expected_filter = Filter([filter_field])
    assert new_filter == expected_filter

def test_immutability_in_add_field(filter_field):
    filter = Filter()
    new_filter = filter.add_field(filter_field)
    assert filter != new_filter
