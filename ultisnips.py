#!/usr/bin/env python
# encoding: utf-8

def parse_args(args):
    if args.startswith(","):
        return parse_args(args[1:])
    #end if
    if args.startswith(" "):
        return parse_args(args[1:])
    #end if
    if args.startswith("["):
        return "${" + tab_stop_number + parse_args() + "}"
    #end if
#end def

def ultisnips(file, trigger, prefix):
    """Extra functions/methods/text from a text file to generate snippets.
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
    snip = "snippet " + trigger + " \"Methods of " + trigger +"\" !b\n" 
    snip += "${2:" + trigger + "}$1`!p snip.rv = complete(t[1], [" + ", ".join(methods) + "])`\n"
    snip += "endsnippet\n"
    print(snip)
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
    return 0 if prefix == "" else len(prefix) + 1
#end def

if __name__ == '__main__':
    import sys
    sys.argv.pop(0)
    ultisnips(sys.argv, None, None)
#end if
