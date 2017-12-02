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

def main(args):
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
    extraSymbol = "("
    triggerInTabStop = False
    optlist, args = getopt.gnu_getopt(args, 'f:t:p:e:Th')
    for o,v in optlist:
        if o == "-f":
            file = v
            continue
        if o == "-t":
            trigger = v
            #print("trigger: " + trigger)
            continue
        if o == "-p":
            prefix = v
            continue
        if o == "-e":
            extraSymbol = v
            continue
        if o == "-T":
            triggerInTabStop = True
            continue
        if o == "-h":
            help()
            return
    #end for
    n = len(args)
    if n > 1:
        warnings.warn("Too many independent arguments!")
        return
    if n == 1:
        file = args[0]
    ultisnips.ultisnips(file, trigger, prefix, extraSymbol, triggerInTabStop)

if __name__ == '__main__':
    sys.argv.pop(0)
    main(sys.argv)
