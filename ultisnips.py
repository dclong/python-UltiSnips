#!/usr/bin/env python
# encoding: utf-8
import warnings
import re

def parseArgs(args, tab_stop_index):
    if args == "":
        return ""
    #end if
    if args.startswith(","):
        return "," + parseArgs(args[1:], tab_stop_index)
    #end if
    if args.startswith(" "):
        return " " + parseArgs(args[1:], tab_stop_index)
    #end if
    if args.startswith("["):
        if args.endswith("]"):
            return "${" + str(tab_stop_index) + ":" + parseArgs(args[1:-1], tab_stop_index+1) + "}"
        #end if
        warnings.warn('Mal-formatted brackets in "' + args + '"!')
        return ""
    #end if
    index = endOfFirstArg(args)
    return "${" + str(tab_stop_index) + ":" + args[:index] + "}" + parseArgs(args[index:], tab_stop_index+1)
#end def

def endOfFirstArg(args):
    n = len(args)
    for i in range(n):
        char = args[i]
        if char=="[" or char==",":
            return i
        #end if
    #end for
    return n
#end def

def ultiSnips(file, trigger, prefix, extraSymbol, triggerInTabStop):
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
    methods = ['"' + methodName(line, prefix) + '"' for line in lines]
    snip = "global !p\nfrom complete import *\nendglobal\n\n"
    snip += "snippet " + trigger + " \"Methods of " + trigger +"\" b\n" 
    if triggerInTabStop:
        snip += "${2:" + trigger + "}"
    else:
        snip += trigger 
    #end if
    snip += "$1`!p snip.rv = complete(t[1], [" + ", ".join(methods) + "])`\n"
    snip += "endsnippet\n"
    snips = [snip]
    for line in lines:
        snips.append("\n" + methodSnippet(line, prefix, trigger, extraSymbol, triggerInTabStop))
    #end for
    snips = [snip for snip in snips if snip.strip()!=""]
    snips = "".join(snips)
    print(snips)
#end def 

def methodSnippet(line, prefix, trigger, extraSymbol, triggerInTabStop):
    '''Generate snippet for a method/function in a module.
    '''
    begin = line.find("(")   
    if begin != -1:
        end = line.find(")")
        method = methodName(line, prefix)
        tm = trigger + method
        extraSymbol = normalizeExtraSymbol(extraSymbol)
        if extraSymbol != "":
            snip = 'snippet "\\b' + tm + extraSymbol + '?" "' + tm + '" r\n' 
        else:
            snip = 'snippet ' + tm + ' "' + tm + '" w\n' 
        #end if
        if triggerInTabStop:
            snip += "${1:" + trigger + "}" + method + "(" + parseArgs(line[begin+1:end], 2) + ")\n"
            snip += "endsnippet\n"
        else:
            snip += tm + "(" + parseArgs(line[begin+1:end], 1) + ")\n"
            snip += "endsnippet\n"
        #end if
        return snip
    #end if
    return ""
#end def

def normalizeExtraSymbol(symbol):
    escapes = ["*", "?", ".", "+", "^", "$", "\\", "|", ")", "(", "[", "]"]
    if symbol in escapes:
        return "\\"  + symbol
    #end if
    return symbol
#end def

def methodName(line, prefix):
    '''Extract the method name from a line in the help document.
    '''
    delimiter = "("
    if delimiter in line:
        return line[len(prefix):line.index(delimiter)]
    #end if
    delimiter = " "
    if delimiter in line:
        return line[len(prefix):line.index(delimiter)]
    #end if
    return line[len(prefix):].strip()
#end def
