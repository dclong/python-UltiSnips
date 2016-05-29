import arguments

def method_snippet_1(trigger, method, extra_symbol):
    trigger += method
    extra_symbol = normalize_extra_symbol(extra_symbol)
    if extra_symbol != "":
        return 'priority 10\nsnippet "\\b' + trigger + extra_symbol + '?" "' + trigger + '" r\n' 
    #end if
    return 'priority 10\nsnippet ' + trigger + ' "' + trigger + '" w\n' 
#end def

def method_snippet_2(trigger, method, args, trigger_in_tab_stop):
    if trigger_in_tab_stop:
        snip = method + "(" + arguments.parse_args(args, True) + ")\n"
        if trigger.endswith("."):
            return "${" + str(arguments.parse_args.__tab_stop_index__) + ":" + trigger[:-1] + "}." + snip
        #end if
        return "${" + str(arguments.parse_args.__tab_stop_index__) + ":" + trigger + "}" + snip
    #end if
    return trigger + method + "(" + arguments.parse_args(args, True) + ")\n"
#end def

def method_snippet(line, prefix, trigger, extra_symbol, trigger_in_tab_stop):
    '''Generate snippet for a method/function in a module.
    '''
    begin = line.find("(")   
    if begin != -1:
        end = line.find(")")
        method = method_name(line, prefix)
        snip = method_snippet_1(trigger, method, extra_symbol) \
                + method_snippet_2(trigger, method, line[begin+1:end], trigger_in_tab_stop) \
                + "endsnippet\n"
        return snip
    #end if
    return ""
#end def

def normalize_extra_symbol(symbol):
    escapes = ["*", "?", ".", "+", "^", "$", "\\", "|", ")", "(", "[", "]"]
    if symbol in escapes:
        return "\\"  + symbol
    #end if
    return symbol
#end def

def method_name(line, prefix):
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
