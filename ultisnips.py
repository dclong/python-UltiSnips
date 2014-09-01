#!/usr/bin/env python
# encoding: utf-8
import warnings

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

def ultisnips(file, trigger, prefix):
    """Extract functions/methods/text from a text file to generate snippets.
    ( and a blank space are used as delimiters to extract names of functions/methods. 

    :trigger prefix of triggering snippets.
    :prefix prefix of function/method/text as the patten. 
    :returns: @todo

    """
    import re
    if type(file) == list:
        n = len(file)
        if n == 3:
            ultisnips(file[0], file[1], file[2])
            return
        #end if
        if n == 2:
            ultisnips(file[0], file[1], "")
            return
        #end if
        print("Wrong number of arguments!")
        return
    #end if
    f = open(file, 'r')
    lines = f.readlines() 
    # default pattern
    p1 = prefix + "\w+"
    p2 = prefix + "\w+\(.*\)"
    pattern = p1 + "|" + p2
    pattern = re.compile(pattern)
    lines = [line for line in lines if pattern.match(line) != None]
    methods = ['"' + methodName(line, prefix) + '"' for line in lines]
    snip = "snippet " + trigger + " \"Methods of " + trigger +"\" b\n" 
    snip += "${2:" + trigger + "}$1`!p snip.rv = complete(t[1], [" + ", ".join(methods) + "])`\n"
    snip += "endsnippet\n"
    snips = [snip]
    for line in lines:
        snips.append("\n" + methodSnippet(line, prefix, trigger))
    #end for
    snips = [snip for snip in snips if snip.strip()!=""]
    snips = "".join(snips)
    print(snips)
#end def 

def methodSnippet(line, prefix, trigger):
    begin = line.find("(")   
    if begin != -1:
        end = line.find(")")
        method = methodName(line, prefix)
        method = trigger + method
        snip =  "snippet " + method + ' "' + method + "\" b\n" 
        snip += method + "(" + parseArgs(line[begin+1:end], 1) + ")\n"
        snip += "endsnippet\n"
        return snip
    #end if
    return ""
#end def

def methodName(line, prefix):
    delimiter = "("
    if delimiter in line:
        return line[startIndex(prefix):line.index(delimiter)]
    #end if
    delimiter = " "
    if delimiter in line:
        return line[startIndex(prefix):line.index(delimiter)]
    #end if
    return line[startIndex(prefix):].strip()
#end def

def startIndex(prefix):
    return 0 if prefix == "" else len(prefix)
#end def

if __name__ == '__main__':
    import sys
    sys.argv.pop(0)
    ultisnips(sys.argv, None, None)
#end if
