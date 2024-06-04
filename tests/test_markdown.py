
from pyobsidian.markdown import MkHeaderLevels
from deepdiff import DeepDiff

def test_get_levels():
    markdown = '''
    # Title 1
    ## Title 1-1
    # Title 2
    # Title 3
    ## Title 3-1
    '''
    levels = MkHeaderLevels(markdown).get_levels()
    expected = {
        '1': [
            {'start': 5, 'end': 14, 'content': 'Title 1'},
            {'start': 36, 'end': 45, 'content': 'Title 2'},
            {'start': 50, 'end': 59, 'content': 'Title 3'}
        ], 
        '2': [
            {'start': 19, 'end': 31, 'content': 'Title 1-1'},
            {'start': 64, 'end': 76, 'content': 'Title 3-1'}
        ]
    }
    assert DeepDiff(levels, expected, ignore_order=True) == {}
