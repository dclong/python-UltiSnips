import argument as arg
import re

def snippet(line, prefix, trigger, extra_symbol, trigger_tab):
    '''Generate snippet for a method/function in a module.
    '''
    if not '(' in line:
        return ''
    s = '''
priority 10
snippet "\\b{trigger}{extra_symbol}" "{name}" r 
{tab_trigger}{method}({args})
endsnippet
'''
    method = name(line, prefix)
    s = s.format(
        trigger = trigger + method,
        extra_symbol = _normalize_symbol(extra_symbol),
        name = method,
        method = method,
        tab_trigger = _tab_trigger(trigger, trigger_tab),
        args = arg.parse(line, True)
    )
    return s
#end def

def _tab_trigger(trigger, trigger_tab):
    s = ''
    if trigger_tab:
        s = '${index:trigger}'
        s = s.replace('index', str(arg.parse._index))
        s = s.replace('trigger', trigger)
    return s

def _normalize_symbol(symbol):
    if symbol == '':
        return ''
    escapes = [
        "*",
        "?",
        ".",
        "+",
        "^",
        "$",
        "\\",
        "|",
        ")",
        "(",
        "[",
        "]"
    ]
    if symbol in escapes:
        symbol = '\\'  + symbol
    return symbol + '?'

def name(line, prefix):
    m = _name(line, prefix)
    return _clean(m)

def _clean(method):
    method = re.sub('\[.*\]', '', method)
    method = re.sub(':.*$', '', method)
    return method.strip()

def _name(line, prefix):
    '''Extract the method name from a line in the help document.
    '''
    prefix = '^(' + prefix + ')'
    line = re.sub(prefix, '', line)
    delimiter = "("
    if delimiter in line:
        return line[:line.index(delimiter)]
    delimiter = " "
    if delimiter in line:
        return line[:line.index(delimiter)]
    return line.strip()
#end def
