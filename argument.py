import warnings

def parse(line, reset):
    if reset:
        parse._index  = 1
    args = _args(line)
    if args == '':
        return ''
    if args.startswith(","):
        return "," + parse(args[1:], False)
    if args.startswith(" "):
        return " " + parse(args[1:], False)
    if args.startswith("["):
        if args.endswith("]"):
            args = args[1:-1]
            snip = "${" + str(parse._index) + ":" 
            parse._index += 1
            if _end_arg(args) >= len(args):
                return snip + args + "}"
            #end if
            return snip + parse(args, False) + "}"
        #end if
        warnings.warn('Mal-formatted brackets in "' + args + '"!')
        return ""
    #end if
    index = _end_arg(args)
    snip = "${" + str(parse._index) + ":" + args[:index] + "}" 
    parse._index += 1
    snip += parse(args[index:], False)
    return snip

def _end_arg(args):
    '''Find end index of the (first) argument.
    '''
    n = len(args)
    for i in range(n):
        char = args[i]
        if char in ('[', ','):
            return i
    return n

def _args(line):
    begin = line.find('(')   
    end = line.find(")")
    return line[begin+1:end].strip()
