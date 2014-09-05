#!/usr/bin/env python
# encoding: utf-8
import warnings
import re
import method

def ultiSnips(file, trigger, prefix, extra_symbol, trigger_in_tab_stop):
    '''Extract functions/methods/text from a text file to generate snippets.
    ( and a space are used as delimiters to extract names of functions/methods. 

    :trigger prefix of triggering snippets.
    :prefix prefix of function/method/text as the patten. 
    :returns: @todo

    '''
    f = open(file, 'r')
    lines = f.readlines() 
    # default pattern
    p1 = prefix + "\w+"
    p2 = prefix + "\w+\(.*\)"
    pattern = p1 + "|" + p2
    pattern = re.compile(pattern)
    lines = [line for line in lines if pattern.match(line) != None]
    methods = ['"' + method.method_name(line, prefix) + '"' for line in lines]
    snip = "global !p\nfrom complete import *\nendglobal\n\n"
    snip += "snippet " + trigger + " \"Methods of " + trigger +"\" b\n" 
    if trigger_in_tab_stop:
        snip += "${2:" + trigger + "}"
    else:
        snip += trigger 
    #end if
    snip += "$1`!p snip.rv = complete(t[1], [" + ", ".join(methods) + "])`\n"
    snip += "endsnippet\n"
    snips = [snip]
    for line in lines:
        snips.append("\n" + method.method_snippet(line, prefix, trigger, extra_symbol, trigger_in_tab_stop))
    #end for
    snips = [snip for snip in snips if snip.strip()!=""]
    snips = "".join(snips)
    print(snips)
#end def 

