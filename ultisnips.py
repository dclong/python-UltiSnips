#!/usr/bin/env python
# encoding: utf-8
import method
import warnings
import re
import json
import os

def _extract_lines(file, prefix):
    with open(file, 'r') as f:
        lines = f.readlines() 
    prefix = '(' + prefix + ')'
    p1 = prefix + "\w+"
    p2 = prefix + "\w+\(.*\)"
    pattern = re.compile(p1 + "|" + p2)
    return [line for line in lines if pattern.match(line) != None]

def _methods( lines, prefix, file_json):
    methods = set(method.name(line, prefix) for line in lines)
    methods = [m for m in methods if m != '']
    methods.sort()
    with open(file_json, 'w') as f:
        json.dump(methods, f, indent=4)
    return ['"' + m + '"' for m in methods]

def _snippet_complete(trigger, file_json, trigger_tab):
    snip = '''
global !p
from complete import *
endglobal

priority 10
snippet "\\b{trigger}" "Methods of {name}" r 
{tab2}$1`!p snip.rv = complete(t[1], file='{file_json}')`
endsnippet

'''
    tab2 = '${2:' + trigger + '}' if trigger_tab else ''
    snip = snip.format(
        trigger = re.sub('\.$', '\.', trigger),
        name = re.sub('\.$', '', trigger),
        tab2 = tab2,
        file_json = file_json
    )
    return snip

def ultisnips(file, trigger, prefix, extra_symbol, trigger_tab):
    '''Extract functions/methods/text from a text file to generate snippets.
    ( and a space are used as delimiters to extract names of functions/methods. 

    :trigger prefix of triggering snippets.
    :prefix prefix of function/method/text as the patten. 
    :extra_symbol
    :trigger_tab boolean; whether to have the trigger in a tab stop.
    :returns: @todo

    '''
    title = os.path.splitext(os.path.basename(file))[0] 
    file_json = title + '.json'
    lines = _extract_lines(file, prefix)
    methods = _methods(lines, prefix, file_json)
    s0 = _snippet_complete(trigger=trigger, file_json=file_json, trigger_tab=trigger_tab)
    snips = (method.snippet(line, prefix, trigger, extra_symbol, trigger_tab) for line in lines)
    s1 = ''.join(s for s in snips if s.strip() != '')
    s = s0 + s1
    with open(title + '.snippets', 'w') as f:
        f.write(s)
    print(s)
