
__all__ = ["iskeyword", "kwlist"]

kwlist = [
    'print',
    'input',
    'integer',
    'string',
    'if',
    'elif',
    'while',
    'continue',
    'pip'
]
iskeyword = frozenset(kwlist).__contains__