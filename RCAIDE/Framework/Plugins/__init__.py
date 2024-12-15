import os

if os.getenv('SPHINX_BUILD', '0') == '1':
    pass
else:
    from .load_plugin import load_plugin
    pint = load_plugin('pint')
