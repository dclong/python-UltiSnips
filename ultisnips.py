#!/usr/bin/env python
# encoding: utf-8

def ultisnips(file, prefix, sniprefix):
    """@todo: Docstring for ultisnips.

    :param prefix prefix of method (excluding the dot) as the patten. 
    :sniprefix prefix of triggering snippets (excluding the dot).
    :returns: @todo

    """
    import re
    if type(file) == list:
        n = len(file)
        if n != 3:
            print("Wrong number of arguments!")
            return
        #end if
        ultisnips(file[0], file[1], file[2])
        return
    #end if
    f = open(file, 'r')
    lines = f.readlines() 
    pattern = "\w+\(.*\)"
    if prefix != "":
        pattern = prefix + "\.\w+|" + prefix + "\." + pattern
    #end if
    pattern = re.compile(pattern)
    lines = [line for line in lines if pattern.match(line) != None]
    methods = ['"' + methodName(line, prefix) + '"' for line in lines]
    snip = "snippet " + sniprefix + ". \"Methods of " + sniprefix +"\"\n" 
    snip += "${2:" + sniprefix + "}.$1`!p snip.rv = complete(t[1], [" + ", ".join(methods) + "])`\n"
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
