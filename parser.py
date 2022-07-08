
def parse(cc, conversion, delim=' ', ctx=[]):

    raw_args = cc.strip().split(delim)

    try:
        CMD = conversion[raw_args[0]]
    except KeyError:
        print("Unknown Command %s" % raw_args[0])
        CMD = ""

    RAW_ARGS = raw_args[1:]
    STR_ARGS = delim.join(RAW_ARGS)
    try:
        P_ARGS = [ctx[int(i)] for i in RAW_ARGS]
    except IndexError:
        P_ARGS = ctx

    return {"CMD":CMD, "RAW_ARGS":RAW_ARGS, "STR_ARGS":STR_ARGS, "PARSED_ARGS":P_ARGS}

