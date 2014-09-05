#!/usr/bin/env python
# encoding: utf-8

import ultisnips
import sys
import getopt
import warnings

def help():
    print((
        "Syntax: ultisnips -t trigger [options] [-f] doc\n"
        "-f file: The file containing help document.\n"
        "-t trigger: The trigger to be used. The default value is trigger.\n"
        "-p prefix: Prefix pattern in the help document. The default value is blank\n"
        "-e symbol: Add an optional extra symbol to the trigger (to avoid confliction). "
        "The default value is blank."
        "-T Put the trigger in to a tab stop.\n"
        "-h Print help message and exit.\n"
        "Examples\n"
        "ultisnips -t getopt. -p getopt. -s getopt.txt"
        ))
#end def
def runUltiSnips(args):
    '''Run underlying workhorse ultiSnips to generate snippets.
    -f file: The file containing help document.
    -t trigger: The trigger to be used.
    -p prfix: Prefix in the help document. The default value is blank.
    -e symbol: Add an optional extra symbol to the trigger (to avoid confliction). "
    "The default value is blank."
    -T Put the trigger in to a tab stop.
    -h Print help message and exit.
    '''
    trigger = "trigger"
    prefix = ""
    extraSymbol = "[a-zA-Z]"
    triggerInTabStop = False
#    print(args)
    optlist, args = getopt.gnu_getopt(args, 'f:t:p:e:Th')
#    print(optlist)
#    print(args)
    for opt in optlist:
        o = opt[0]
        v = opt[1]
        if o == "-f":
            file = v
            continue
        #end if
        if o == "-t":
            trigger = v
            #print("trigger: " + trigger)
            continue
        #end if
        if o == "-p":
            prefix = v
            continue
        #end if
        if o == "-e":
            extraSymbol = v
            continue
        #end if
        if o == "-T":
            triggerInTabStop = True
            continue
        #end if
        if o == "-h":
            help()
            return
        #end if
    #end for
    n = len(args)
    if n > 1:
        warnings.warn("Too many independent arguments!")
        return
    #end if
    if n == 1:
        file = args[0]
    #end if
    ultisnips.ultiSnips(file, trigger, prefix, extraSymbol, triggerInTabStop)
#end def

if __name__ == '__main__':
    sys.argv.pop(0)
    runUltiSnips(sys.argv)
#end if
