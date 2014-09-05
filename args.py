import warnings
def parse_args(args, reset):
    if reset:
        parse_args.__tab_stop_index__  = 1
    #end if
    if args == "":
        return ""
    #end if
    if args.startswith(","):
        return "," + parse_args(args[1:], False)
    #end if
    if args.startswith(" "):
        return " " + parse_args(args[1:], False)
    #end if
    if args.startswith("["):
        if args.endswith("]"):
            snip = "${" + str(parse_args.__tab_stop_index__) + ":" 
            parse_args.__tab_stop_index__ += 1
            snip += parse_args(args[1:-1], False) + "}"
            return snip
        #end if
        warnings.warn('Mal-formatted brackets in "' + args + '"!')
        return ""
    #end if
    index = end_of_first_arg(args)
    snip = "${" + str(parse_args.__tab_stop_index__) + ":" + args[:index] + "}" 
    parse_args.__tab_stop_index__ += 1
    snip += parse_args(args[index:], False)
    return snip
#end def

def end_of_first_arg(args):
    n = len(args)
    for i in range(n):
        char = args[i]
        if char=="[" or char==",":
            return i
        #end if
    #end for
    return n
#end def

