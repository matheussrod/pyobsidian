def read_file(path: str) -> str:
    """Read the content of a file.

    Parameters
    ----------
    path : str
        The path of the file to be read.

    Returns
    -------
    str
        The content of the file.
    """
    with open(path, 'r', encoding='utf8') as file:
         content = file.read()
    return content
